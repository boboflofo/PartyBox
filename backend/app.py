from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, send, leave_room, join_room, emit
from flask_cors import CORS
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
socketio = SocketIO(app,cors_allowed_origins="*")
CORS(app, resources={r"/*": {"origins": "*"}})

rooms = {}

@app.route('/')
def serve_react():
    return send_from_directory('..', 'my-react-app/build/index.html')

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('get_room_players')
def get_room_players(room_id):
    if room_id in rooms:
        emit('room_players_update', {'room_id': room_id, 'players': list(rooms[room_id].values())})
    else:
        emit('room_not_found')

@socketio.on('host_room')
def host_room(data):
    room_id = generate_unique_code(6)
    player_name = data['player_name']  
    rooms[room_id] = {request.sid: player_name}
    emit('room_created', {'room_id': room_id}, broadcast=True)
    print(rooms)

@socketio.on('join_room')
def join_room(data):
    if 'room_id' in data and 'player_name' in data:
        room_id = data['room_id']
        player_name = data['player_name']
        if room_id in rooms:
            rooms[room_id][request.sid] = player_name
            emit('player_joined', {'players': list(rooms[room_id].values())}, room=room_id)
            emit('room_joined', {'room_id': room_id})
        else:
            emit('room_not_found')
    else:
        emit('invalid_data')
    print(rooms)
    


if __name__ == "__main__":
    socketio.run(app, debug=True)



