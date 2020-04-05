function main() {
    socket = io();

    video = document.getElementById("thevideo");
    var roomname = window.location.href.match('/room/(.*)$')[1];
    console.log(roomname);
    var lastseek = 0;
    var seeking = false;
    var lock = false;

    socket.on('connect', function(time) {
        console.log(socket.id);
        socket.emit('join', {'room': roomname});
    });

    function seek(json) {
        if (json.sid != socket.id) {
            if (lastseek != json.time) {
                seeking = true;
                video.currentTime = json.time;
            }
        }
    }

    function emitseek(time, evt) {
        lastseek = time;
        evt = evt ? evt : 'seek';
        socket.emit(evt, {
            'time': time});
    }

    socket.on('seek', seek);

    socket.on('play', (json) => {
        if (json.sid != socket.id) {
            lock = true;
            video.play().then(() => {lock = false});
        }

    });
    socket.on('pause', (json) => {
        if (json.sid != socket.id) {
            var callback = video.onpause;
            lock = true;
            video.pause();
        }

    });

    video.onpause = function(evt) {
        var newtime = video.currentTime;
        if (! lock) {
            socket.emit('pause');
        } else {
            lock = false;
        }
    };

    video.onplay = function(evt) {
        var newtime = video.currentTime;
        if (! lock) {
            socket.emit('play');
        }
    };

    video.onseeked = function(evt) {
        if (seeking) {
            seeking = false;
        } else {
            var newtime = video.currentTime;
            emitseek(newtime, 'seek');
        }
    };
}

window.onload = main;
