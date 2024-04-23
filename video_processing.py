import os
import numpy as np
import requests
from flask import jsonify
import cv2

def decode_video_frame(video_frame):
    # Convert bytes to a NumPy array
    nparr = np.frombuffer(video_frame, np.uint8)
    # Decode the NumPy array into an OpenCV image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def recognize_gesture(video_frame):
    print("Type of video_frame:", type(video_frame))
    model_endpoint = os.getenv("RECOGNIZER_MODEL_ENDPOINT") + "/gesture-recognizer/process-image"
    if not video_frame:
        return jsonify({"error": "Missing video frame for gesture recognition"}), 400
    
    # Decode the bytes to an OpenCV image
    img = decode_video_frame(video_frame)

    # Make a request to the gesture recognition model
    ret, buffer = cv2.imencode('.jpg', img)

    try:
        response = requests.post(
            model_endpoint,
            files={"file": ("frame.jpg", buffer.tobytes(), "image/jpeg")}
        )
        # print("gesture", response)
        if response.status_code == 200:
            result = response.json()
            print("Gesture recognition result:", result)
            # print("Gesture recognition result:", result)
            return result
        else:
            return (
                jsonify(
                    {
                        "error": f"Error calling the gesture recognition model: {response.status_code}"
                    }
                ),
                500,
            )
    
    except requests.RequestException as e:
        return (
            jsonify({"error": f"Error calling the gesture recognition model: {str(e)}"}),
            500,
        )
    