from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import os
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

# Dictionary to store active rooms
rooms = {}

# Serve the index.html file for the root URL
@app.route('/')
def serve_react():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build'), 'index.html')

# Serve static files (JS, CSS, etc.) from subdirectories
@app.route('/static/js/<path:path>')
def serve_js(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static', 'js'), path)

@app.route('/static/css/<path:path>')
def serve_css(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static', 'css'), path)

# Serve image files from the static directory
@app.route('/static/media/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static',  'media'), path)

# Serve manifest.json
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build'), 'manifest.json')

def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# SocketIO event to host a room
@socketio.on('host_room')
def host_room():
    room_id = generate_room_id()
    rooms[room_id] = {}
    emit('room_created', {'room_id': room_id})

# SocketIO event to join a room
@socketio.on('join_room')
def join_room(data):
    room_id = data['room_id']
    if room_id in rooms:
        emit('room_joined', {'room_id': room_id})
    else:
        emit('room_not_found')

if __name__ == "__main__":
    socketio.run(app, debug=True)