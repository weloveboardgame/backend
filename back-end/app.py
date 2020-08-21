from flask import Flask, render_template, session, redirect, request, copy_current_request_context, url_for
from flask_socketio import SocketIO, emit, join_room, rooms, disconnect

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

usercount = 0

board = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,2,0],
    [0,0,0,0,1,1,2]
]

@app.before_request
def before_request():
    if usercount == 2:
        return "X"
    
@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/close')
def close():
    return redirect(url_for('close.htm'))

@socketio.on('my_event', namespace='/test')
def test_message(message):
    emit('my_response', {'data': message['data'], 'board': board})

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    emit('my_response', {'data': 'In rooms: '.join(rooms())})

@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    print(message)
    #emit('my_response', {'data': message['data']}, room=message['room'])

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
    emit('my_response', {'data': 'Disconnected!'}, callback=can_disconnect)

@socketio.on('connect', namespace='/test')
def test_connect():
    global usercount
    print(usercount)
    if usercount == 0 or usercount == 1:
        emit('my_response', {'data': 'Connected', 'count': 0})
        usercount += 1
    elif usercount == 2:
        return "X"

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global usercount
    usercount -= 1
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app)