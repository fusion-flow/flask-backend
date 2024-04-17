from flask_socketio import emit
from classification import perform_classification
from audio_processing import transcribe_audio
import os


def handle_connect():
    print("Client connected")
    print("===================")


def handle_disconnect():
    print("Client disconnected")


def handle_message(message):
    print("message:", message)
    urls = perform_classification(message)
    print("urls", urls)

    emit("response", urls)


def handle_audio_message(message):
    text_message = message["message"]
    audio_blob = message["audio"]
    print("text input ",text_message)
    transcribed_text, status_code = transcribe_audio(audio_blob)
    print("transcribed_text", transcribed_text)
    urls = perform_classification(transcribed_text)
    # print("query_result", query_result)
    emit("audio_message", urls)


def handle_video_message(video_blob):
    print("video blob recieved")
    file_path = "video_frame.jpeg"
    with open(file_path, "wb") as f:
        f.write(video_blob)

    emit("video_message", "hello video")
