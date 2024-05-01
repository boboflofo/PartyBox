from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random
from string import ascii_uppercase
from threading import Timer

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
socketio = SocketIO(app, cors_allowed_origins="*")
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
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
        "answer": "Pacific Ocean"
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["H2O", "CO2", "NaCl", "O2"],
        "answer": "H2O"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Michelangelo"],
        "answer": "Leonardo da Vinci"
    },
    {
        "question": "What year did World War I begin?",
        "options": ["1914", "1917", "1939", "1941"],
        "answer": "1914"
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Tokyo", "Kyoto", "Osaka", "Seoul"],
        "answer": "Tokyo"
    },
    {
        "question": "Who developed the theory of relativity?",
        "options": ["Albert Einstein", "Isaac Newton", "Stephen Hawking", "Galileo Galilei"],
        "answer": "Albert Einstein"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Blue Whale", "African Elephant", "Giraffe", "Hippopotamus"],
        "answer": "Blue Whale"
    },
    {
        "question": "Who was the first man to walk on the moon?",
        "options": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Alan Shepard"],
        "answer": "Neil Armstrong"
    }
    # Add more questions as needed
]

def generate_unique_code(length):
    while True:
        code = "".join(random.choices(ascii_uppercase, k=length))
        if code not in rooms:
            break
    return code

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

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
            emit('room_players_update', {'room_id': room_id, 'players': list(rooms[room_id].values())}, broadcast=True)
            emit('room_joined', {'room_id': room_id})
            print("Room players updated:", rooms[room_id])
        else:
            emit('room_not_found')
    else:
        emit('invalid_data')

@socketio.on('start_game')
def start_game(room_id):
    question = random.choice(questions)
    emit('new_question', question)
    
    if room_id in rooms:
        rooms[room_id]["question"] = question
        if room_id not in timers:
            start_timer(room_id)  # Start the timer only if it hasn't been started before
    else:
        rooms[room_id] = {"question": question, "scores": {}}
        start_timer(room_id)  # Always start the timer for a new room

@socketio.on('answer')
def handle_answer(data):
    room_id = data['room_id']
    answer = data['option']
    
    if room_id in rooms and "question" in rooms[room_id]:
        question = rooms[room_id]["question"]
        correct_answer = question['answer']

        player_sid = data['sid']
        player_name = rooms[room_id][player_sid]
        
        if answer == correct_answer:
            if "scores" in rooms[room_id]:
                if player_name in rooms[room_id]["scores"]:
                    rooms[room_id]["scores"][player_name] += 1
                else:
                    rooms[room_id]["scores"][player_name] = 1
            else:
                rooms[room_id]["scores"] = {player_name: 1}
        else:
            # Penalize incorrect answers (optional)
            if "scores" in rooms[room_id]:
                if player_name in rooms[room_id]["scores"]:
                    rooms[room_id]["scores"][player_name] -= 1  # Decrease score for incorrect answer
                else:
                    rooms[room_id]["scores"][player_name] = -1  # Set score to -1 for incorrect answer
            else:
                rooms[room_id]["scores"] = {player_name: -1}  # Set score to -1 for incorrect answer
        print(rooms[room_id]["scores"])
        emit('update_scores', rooms[room_id]["scores"])

@socketio.on('start_timer')
def start_timer(room_id):
    if room_id not in timers:
        print("Starting timer for room:", room_id)  # Debugging print
        room_timer = Timer(30, game_finished, args=[room_id])
        timers[room_id] = room_timer
        room_timer.start()
        emit('start_timer', broadcast=True)
    else:
        # Restart the timer if it already exists
        print("Restarting timer for room:", room_id)  # Debugging print
        timers[room_id].cancel()  # Cancel the existing timer
        room_timer = Timer(30, game_finished, args=[room_id])
        timers[room_id] = room_timer
        room_timer.start()

def stop_timer(room_id):
    if room_id in timers:
        print("Stopping timer for room:", room_id)  # Debugging print
        timers[room_id].cancel()
        del timers[room_id]
        emit('stop_timer', broadcast=True)
    else:
        print("Timer not found for room:", room_id)  # Debugging print

@socketio.on('game_finished')
def game_finished(room_id):
    print("Game finished for room:", room_id)  # Debugging print
    if room_id in rooms:
        if "scores" in rooms[room_id] and rooms[room_id]["scores"]:
            winner = max(rooms[room_id]["scores"], key=rooms[room_id]["scores"].get)
            emit('game_finished', winner, room=room_id)
        else:
            emit('game_finished', "No winner", room=room_id)  # Emit a message indicating no winner
        
        # Stop the timer by emitting 'stop_timer' event
        emit('stop_timer', room=room_id)  # Emit stop_timer event directly here
        
        # Remove the question from the room
        del rooms[room_id]["question"]
        
        # Notify clients to disable answering
        emit('disable_answer', room=room_id)

if __name__ == "__main__":
    socketio.run(app, debug=True)



