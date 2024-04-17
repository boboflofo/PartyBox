from flask import Flask, send_from_directory
import os

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)