from flask_socketio import emit
from classification import perform_classification
from audio_processing import transcribe_audio
import os

from fusion import fuse_intents


def handle_connect():
    print("Client connected")
    print("===================")


def handle_disconnect():
    print("Client disconnected")


def handle_message(message):
    print("message:", message)
    intents = perform_classification(message)
    fused_intents = fuse_intents(intents, [])
    print("fused_intents", fused_intents)


def handle_audio_message(message):
    text_message = message["message"]
    audio_blob = message["audio"]

    print("text input ",text_message)
    transcribed_text, status_code = transcribe_audio(audio_blob)
    print("transcribed_text", transcribed_text)
    audio_intents = perform_classification(transcribed_text)
    if text_message:
        text_intents = perform_classification(text_message)
    
    fused_intents = fuse_intents(text_intents, audio_intents)
    # print("fused_intents", fused_intents)

    # print("query_result", query_result)
    # emit("audio_message", intents)


def handle_video_message(video_blob):
    print("video blob recieved")
    file_path = "video_frame.jpeg"
    with open(file_path, "wb") as f:
        f.write(video_blob)

    emit("video_message", "hello video")
