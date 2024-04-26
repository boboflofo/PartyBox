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

@socketio.on('host_room')
def host_room(data):
    room_id = generate_unique_code(6)
    player_name = data['player_name']  # Get player name from frontend
    rooms[room_id] = {request.sid: player_name}
    emit('room_created', {'room_id': room_id}, broadcast=True)

@socketio.on('join_room')
def join_room(data):
    if 'room_id' in data and 'player_name' in data:  # Check if both keys are present
        room_id = data['room_id']
        player_name = data['player_name']
        if room_id in rooms:
            print(f"Room '{room_id}' found.")
            join_room(room_id)
            rooms[room_id][request.sid] = player_name
            print(f"Player '{player_name}' joined room '{room_id}'.")
            emit('player_joined', {'player_name': player_name}, room=room_id)
        else:
            print(f"Room '{room_id}' not found.")
            emit('room_not_found')
    else:
        emit('invalid_data')  # Emit an error message if data is incomplete

if __name__ == "__main__":
    socketio.run(app, debug=True)



