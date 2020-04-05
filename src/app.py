from flask import Flask
from flask_socketio import SocketIO, emit
from flask import render_template, request
from flask_socketio import join_room, leave_room, rooms
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/room/<name>')
def room(name):
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit(request.sid + ' joined the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit(request.sid + ' left the room.', room=room)

@socketio.on('seek')
def seek(json):
    json['sid'] = request.sid;
    app.logger.info("SEEK: %s" % json['time']);
    if len(rooms()) == 2:
        room = rooms()[0] if rooms()[0] != request.sid else rooms()[1]
        emit('seek', json, room=room)

@socketio.on('play')
def play():
    app.logger.info("PLAY");
    if len(rooms()) == 2:
        room = rooms()[0] if rooms()[0] != request.sid else rooms()[1]
        emit('play', {'sid': request.sid}, room=room)

@socketio.on('pause')
def pause():
    app.logger.info("PAUSE");
    if len(rooms()) == 2:
        room = rooms()[0] if rooms()[0] != request.sid else rooms()[1]
        emit('pause', {'sid': request.sid}, room=room)

if __name__ == '__main__':
    socketio.run(app)
