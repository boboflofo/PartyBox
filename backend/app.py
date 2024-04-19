from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import random
import string

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="http://localhost:3000")
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

rooms = {}

@app.route('/')
def serve_react():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build'), 'index.html')

@app.route('/static/js/<path:path>')
def serve_js(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static', 'js'), path)

@app.route('/static/css/<path:path>')
def serve_css(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static', 'css'), path)

@app.route('/static/media/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static',  'media'), path)

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build'), 'manifest.json')

def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('host_room')
def host_room():
    room_id = generate_room_id()
    rooms[room_id] = {}
    print(rooms)
    emit('room_created', {'room_id': room_id}, broadcast=True)

@socketio.on('join_room')
def join_room(data):
    room_id = data['room_id']
    if room_id in rooms:
        emit('room_joined', {'room_id': room_id}, broadcast=True)
    else:
        emit('room_not_found')

if __name__ == "__main__":
    socketio.run(app, debug=True)