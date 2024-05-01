from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, send, leave_room, join_room, emit
from flask_cors import CORS
import random
from string import ascii_uppercase
from threading import Timer

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
socketio = SocketIO(app,cors_allowed_origins="*")
CORS(app, resources={r"/*": {"origins": "*"}})

rooms = {}

timers = {}

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["William Shakespeare", "Jane Austen", "Charles Dickens", "Mark Twain"],
        "answer": "William Shakespeare"
    }
]

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
            emit('room_players_update', {'room_id': room_id, 'players': list(rooms[room_id].values())}, broadcast=True)  # Emit room_players_update event immediately
            emit('room_joined', {'room_id': room_id})
            print("Room players updated:", rooms[room_id])  # Print the updated players list
        else:
            emit('room_not_found')
    else:
        emit('invalid_data')
    print(rooms)

@socketio.on('start_game')
def start_game(room_id):
    question = random.choice(questions)
    print(question)
    emit('new_question', question)
    
    if room_id in rooms:
        rooms[room_id]["question"] = question
    else:
        rooms[room_id] = {"question": question, "scores": {}}

@socketio.on('answer')
def handle_answer(data):
    room_id = data['room_id']
    answer = data['option']
    
    # Ensure room exists and has a question
    if room_id in rooms and "question" in rooms[room_id]:
        question = rooms[room_id]["question"]
        correct_answer = question['answer']

        # Check if the answer is correct
        if answer == correct_answer:
            player_sid = data['sid']
            player_name = rooms[room_id][player_sid]  # Get player name from socket ID
            
            # Update scores
            if "scores" in rooms[room_id]:
                if player_name in rooms[room_id]["scores"]:
                    rooms[room_id]["scores"][player_name] += 1  # Increment player's score
                else:
                    rooms[room_id]["scores"][player_name] = 1  # Initialize player's score
            else:
                rooms[room_id]["scores"] = {player_name: 1}  # Initialize scores if not present

            # Emit updated scores to the specific room
            emit('update_scores', rooms[room_id]["scores"])
            stop_timer(room_id)

@socketio.on('start_timer')
def start_timer(room_id):
    # Start the timer for the room
    room_timer = Timer(30, game_finished, args=[room_id])  # 30 seconds timer
    timers[room_id] = room_timer
    room_timer.start()
    emit('start_timer', room=room_id, broadcast=True)

def stop_timer(room_id):
    # Stop the timer for the room
    if room_id in timers and timers[room_id]:
        timers[room_id].cancel()
        del timers[room_id]
        emit('stop_timer', room=room_id)

def game_finished(room_id):
    # Calculate scores, find the winner, and announce it
    if room_id in rooms:
        # Example code to find the winner (you may need to adjust it based on your scoring system)
        winner = max(rooms[room_id]["scores"], key=rooms[room_id]["scores"].get)
        emit('game_finished', winner, room=room_id)

if __name__ == "__main__":
    socketio.run(app, debug=True)



