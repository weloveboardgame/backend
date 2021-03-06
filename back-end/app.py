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
    [0,0,0,0,0,0,0]
]



flag = 1

import random
def getRandGravity():
    tmp = random.randint(0,3)
    res = ''
    if tmp == 0: res = 'N'
    elif tmp == 1: res = 'S'
    elif tmp == 2: res = 'W'
    elif tmp == 3: res = 'E'

    return res

def appplyGravity(board, gravityD):
    if gravityD == 'W':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            k = 0
            for j in range(0, 7):
                if board[i][j] != 0:
                    flag = j
                    break
            for j in range(flag, 7):
                newBoard[i][k] = board[i][j]
                k += 1
        return newBoard
    if gravityD == 'E':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            k = 6
            for j in range(6, -1, -1):
                if board[i][j] != 0:
                    flag = j
                    break
            for j in range(flag, -1, -1):
                newBoard[i][k] = board[i][j]
                k -= 1
        return newBoard
    if gravityD == 'N':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            k = 0
            for j in range(0, 7):
                if board[j][i] != 0:
                    flag = j
                    break
            for j in range(flag, 7):
                newBoard[k][i] = board[j][i]
                k += 1
        return newBoard
    if gravityD == 'S':
        newBoard = [[0 for col in range(7)] for row in range(7)]
        for i in range(0,7):
            flag = 0
            k = 6
            for j in range(6, -1, -1):
                if board[j][i] != 0:
                    flag = j
                    break
            for j in range(flag, -1, -1):
                newBoard[k][i] = board[j][i]
                k -= 1
        return newBoard

def checkGameStatus(board):
    flag = 0
    # 가로세로 판정
    for i in range(7):
        for j in range(4):
            if board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2] and board[i][j] == board[i][j+3] and board[i][j] != 0:
                flag = board[i][j]
            if board[j][i] == board[j+1][i] and board[j][i] == board[j+2][i] and board[j][i] == board[j+3][i] and board[j][i] != 0:
                flag = board[i][j]

    # 우 하향 대각선 판정
    for i in range(4):
        for j in range(4):
            if board[i][j] == board[i+1][j+1] and board[i][j] == board[i+2][j+2] and board[i][j] == board[i+3][j+3] and board[i][j] != 0:
                flag = board[i][j]

    # 좌 하향 대각선 판정
    for i in range(0,4):
        for j in range(3,7):
            if board[i][j] == board[i+1][j-1] and board[i][j] == board[i+2][j-2] and board[i][j] == board[i+3][j-3] and board[i][j] != 0:
                flag = board[i][j]

    return flag

gravity = getRandGravity()

@app.before_request
def before_request():
    if usercount == 2:
        pass
        #return "X"
    
@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/close')
def close():
    return redirect(url_for('close.htm'))

@socketio.on('my_event', namespace='/test')
def test_message(message):
    emit('my_response', {'data': message['data'], 'board': board, 'gravity': gravity})

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    emit('my_response', {'data': 'In rooms: '.join(rooms())})

@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    global flag
    if flag == 1: flag = 2
    else: flag = 1   
    data = message['data']
    gravity = getRandGravity()
    data = appplyGravity(data, gravity)
    emit('my_response', {'data': message['data'], 'board': data, 'gravity': gravity, 'flag':flag}, room=message['room'])
    
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