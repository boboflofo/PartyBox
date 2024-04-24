from flask import Flask, send_from_directory, request, session, redirect
from flask_socketio import SocketIO, send, leave_room, join_room
from flask_cors import CORS
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
socketio = SocketIO(app,cors_allowed_origins="http://localhost:3000")
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

rooms = {}

@app.route('/', methods=["POST", "GET"])
def home():
    return 


# def serve_react():
#     return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build'), 'index.html')

# @app.route('/static/js/<path:path>')
# def serve_js(path):
#     return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static', 'js'), path)

# @app.route('/static/css/<path:path>')
# def serve_css(path):
#     return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static', 'css'), path)

# @app.route('/static/media/<path:path>')
# def serve_static(path):
#     return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build', 'static',  'media'), path)

# @app.route('/manifest.json')
# def serve_manifest():
#     return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'my-react-app', 'build'), 'manifest.json')

# def generate_unique_code(length):
#     while True:
#         code = ""
#         for _ in range(length):
#             code += random.choice(ascii_uppercase)
        
#         if code not in rooms:
#             break
    
#     return code

# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('host_room')
# def host_room():
#     room_id = generate_room_id()
#     rooms[room_id] = {}
#     print(rooms)
#     emit('room_created', {'room_id': room_id}, broadcast=True)

# @socketio.on('join_room')
# def join_room(data):
#     room_id = data['room_id']
#     if room_id in rooms:
#         emit('room_joined', {'room_id': room_id}, broadcast=True)
#     else:
#         emit('room_not_found')

if __name__ == "__main__":
    socketio.run(app, debug=True)



