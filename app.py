# app.py
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO
from flask_cors import CORS
from socket_handlers import (
    handle_connect,
    handle_disconnect,
    handle_message,
    handle_audio_message,
    handle_video_message,
)

# from classification_routes import classification_bp
# from recognition_routes import recognition_bp

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)

# Load environment variables from .env file
load_dotenv()


socketio.on_event("connect", handle_connect)
socketio.on_event("disconnect", handle_disconnect)
socketio.on_event("message", handle_message)
socketio.on_event("audio_message", handle_audio_message)
socketio.on_event("video_message", handle_video_message)


print("CLASSIFICATION_MODEL_ENDPOINT:", os.getenv("CLASSIFICATION_MODEL_ENDPOINT"))
print("RECOGNIZER_MODEL_ENDPOINT:", os.getenv("RECOGNIZER_MODEL_ENDPOINT"))

# app.register_blueprint(classification_bp, url_prefix="/classification")
# app.register_blueprint(recognition_bp, url_prefix="/recognition")


@app.route("/")
def hello_world():
    return "Welcome to FusionFlow backend!"


if __name__ == "__main__":
    socketio.run(app, debug=True)
