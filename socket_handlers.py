from flask_socketio import emit
from classification import perform_classification
from audio_processing import transcribe_audio
import os
import constants
from flask import session

from fusion import fuse_intents
from video_processing import recognize_gesture


def handle_connect():
    print("Client connected")
    print("===================")
    # Initialize session state if not set
    if 'state' not in session:
        session['state'] = constants.NORMAL_STATE


def handle_disconnect():
    print("Client disconnected")

def toggle_status():
    # # print("state before...", session['state'])
    # if session['state'] == constants.NAVIGATION_LIST_STATE:
    #     session['state'] = constants.NAVIGATION_PROCESS_STATE
    #     return
    # if session['state'] == constants.NAVIGATION_PROCESS_STATE:
    #     session['state'] = constants.NORMAL_STATE
    #     return
    # # print("state changed...", session['state'])
    pass

def handle_message(message):
    toggle_status()
    print("state handle", session['state'])
    print("message:", message)
    intents = perform_classification(message)
    fused_intents = fuse_intents(intents, [])
    print("fused_intents", fused_intents)
    # print("state", session['state'])


def handle_audio_message(message):
    toggle_status()
    text_message = message["message"]
    audio_blob = message["audio"]
    audio_intents, text_intents, gesture_intent= [], [], None
    print("text input ",text_message)
    transcribed_text, status_code = transcribe_audio(audio_blob)
    print("transcribed_text", transcribed_text)
    if transcribed_text:
        audio_intents = perform_classification(transcribed_text)
    if text_message:
        text_intents = perform_classification(text_message)

    if session['state'] == constants.NAVIGATION_PROCESS_STATE:
        if session['gesture'] is not None:
            gesture_intent = session['gesture']
    
    fused_intents = fuse_intents(text_intents, audio_intents, gesture_intent)
    print("fused_intents", fused_intents)

    # print("query_result", query_result)
    # emit("audio_message", intents)


def handle_video_message(video_blob):
    toggle_status()
    if session['state'] != constants.NAVIGATION_LIST_STATE:
        return
    file_path = "video_frame.jpeg"
    with open(file_path, "wb") as f:
        f.write(video_blob)
    
    gesture = recognize_gesture(video_blob)
    # {'gesture': 1, 'confidence': 0.4908}
    # check confidence level
    if gesture['confidence'] > 0.5:
        print("gesture intent", gesture['gesture'])
    else:
        print("gesture intent not confident enough")
        if session['gesture']['confidence'] < gesture['confidence']:
            session['gesture'] = gesture


