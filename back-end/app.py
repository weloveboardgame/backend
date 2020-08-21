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
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,1,2]
]

import random
def getRandGravity():
    tmp = random.randint(0,3)
    res = ''
    if tmp == 0: res = 'N'
    if tmp == 1: res = 'S'
    if tmp == 2: res = 'W'
    if tmp == 3: res = 'E'

    return res

def appplyGravity(board, gravityD):
    if gravityD == 'W':
        newBoard = [0 for i in range(7)]
        tempBoard = [0 for i in range(7)]

        for i in range(0,7):
            tempBoard = [0 for i in range(7)]
            flag = 0
            for j in range(0,7):
                if board[i][j] != 0:
                    tempBoard[flag] = board[i][j]
                    flag += 1
            newBoard[i] = tempBoard
        return newBoard
    if gravityD == 'E':
        newBoard = [0 for i in range(7)]
        tempBoard = [0 for i in range(7)]
        for i in range(0,7):
            tempBoard = [0 for i in range(7)]
            flag = 0
            for j in range(0,7):
                if board[i][j] != 0:
                    tempBoard[6-flag] = board[i][j]
                    flag += 1
            newBoard[i] = tempBoard
        return newBoard
    if gravityD == 'N':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            for j in range(0,7):
                if board[j][i] != 0:
                    newBoard[flag][i] = board[j][i]
                    flag += 1
        return newBoard
    if gravityD == 'S':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            for j in range(0,7):
                if board[j][i] != 0:
                    newBoard[6-flag][i] = board[j][i]
                    flag += 1
        return newBoard

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
    emit('my_response', {'data': message['data'], 'board': board, 'gravity' : 'W'})

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    emit('my_response', {'data': 'In rooms: '.join(rooms())})

@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    data = message['data']
    data = appplyGravity(data, "N")
    print(data)
    emit('my_response', {'data': message['data'], 'board': data}, room=message['room'])

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