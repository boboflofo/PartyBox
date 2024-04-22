from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import random
from string import ascii_uppercase

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

# @app.route("/", methods=["POST", "GET"])
# def home():
#     session.clear()
#     if request.method == "POST":
#         name = request.form.get("name")
#         code = request.form.get("code")
#         join = request.form.get("join", False)
#         create = request.form.get("create", False)

#         if not name:
#             return render_template("home.html", error="Please enter a name.", code=code, name=name)

#         if join != False and not code:
#             return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
#         room = code
#         if create != False:
#             room = generate_unique_code(4)
#             rooms[room] = {"members": 0, "messages": []}
#         elif code not in rooms:
#             return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
#         session["room"] = room
#         session["name"] = name
#         return redirect(url_for("room"))

#     return render_template("home.html")
#  @socketio.on("connect")
# def connect(auth):
#     room = session.get("room")
#     name = session.get("name")
#     if not room or not name:
#         return
#     if room not in rooms:
#         leave_room(room)
#         return
    
#     join_room(room)
#     send({"name": name, "message": "has entered the room"}, to=room)
#     rooms[room]["members"] += 1
#     print(f"{name} joined room {room}")

# @socketio.on("disconnect")
# def disconnect():
#     room = session.get("room")
#     name = session.get("name")
#     leave_room(room)

#     if room in rooms:
#         rooms[room]["members"] -= 1
#         if rooms[room]["members"] <= 0:
#             del rooms[room]
    
#     send({"name": name, "message": "has left the room"}, to=room)
#     print(f"{name} has left the room {room}")

