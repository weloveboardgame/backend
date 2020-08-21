from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, join_room, rooms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

full = 0

@app.before_request
def before_request():
    global full
    print(full)
    if full == 2: return "X"
    elif full == 0: full += 1
    elif full == 1: full += 1
    else: full = 1
    
@app.route('/')
def index():
    return render_template('index.htm')

@socketio.on('connect', namespace='/test')
def connect():
    
    print("connected!!")
    emit('my_response', {'data': 'Connected'})

@socketio.on("who", namespace="/test")
def who(data):
    if len(str(data).strip()) == 0:
        return "X"
    else:
        print(data["data"])

@socketio.on('disconnect_request', namespace='/mynamespace') 
def disconnect(): 
    global full
    print(full)
    full -= 1
    return "disconnected.." 

if __name__ == '__main__':
    socketio.run(app)