from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Define a route to serve the React build files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path == "":
        return send_from_directory(os.path.join(os.path.dirname(__file__), 'my-react-app', 'build'), 'index.html')
    else:
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'my-react-app', 'build', path)):
            return send_from_directory(os.path.join(os.path.dirname(__file__), 'my-react-app', 'build'), path)
        else:
            return send_from_directory(os.path.join(os.path.dirname(__file__), 'my-react-app', 'build'), 'index.html')

if __name__ == "__main__":
    app.run(debug=True)