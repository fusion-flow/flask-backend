# app.py
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO
from flask_cors import CORS
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)


# Load environment variables from .env file
load_dotenv()

print("CLASSIFICATION_MODEL_ENDPOINT:", os.getenv("CLASSIFICATION_MODEL_ENDPOINT"))
print("RECOGNIZER_MODEL_ENDPOINT:", os.getenv("RECOGNIZER_MODEL_ENDPOINT"))


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    print("===================")


@socketio.on("disconnect")
def handle_disconnect():
    # disconnect the client
    print("Client disconnected")


@socketio.on("message")
def handle_message(message):
    print("message:", message)
    socketio.emit("message", "hello honeybee")


@socketio.on("audio_message")
def handle_message(audio_blob):
    blob_to_mp3(audio_blob)
    socketio.emit("audio_message", "hello bee")


def blob_to_mp3(blob_data, output_filename='output.mp3'):
    try:
        # Convert blob data to AudioSegment
        audio_segment = AudioSegment.from_file(BytesIO(blob_data))

        # Export the AudioSegment to an MP3 file
        # audio_segment.export(output_filename, format='mp3')

        print(f"Conversion successful. MP3 file saved as '{output_filename}'")
    except Exception as e:
        print(f"Error: {e}")

@app.route("/")
def hello_world():
    return "Welcome to FusionFlow backend!"


@app.route("/classify", methods=["GET"])
def classify():
    if request.method == "GET":
        model_endpoint = os.getenv("CLASSIFICATION_MODEL_ENDPOINT") + "/search"
        print(
            "CLASSIFICATION_MODEL_ENDPOINT:", os.getenv("CLASSIFICATION_MODEL_ENDPOINT")
        )

        query = request.args.get("query", "")

        if not query:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        # Specify the parameters for your request
        params = {
            "query": query,
        }

        # Make a request to the intent classification model
        try:
            response = requests.get(model_endpoint, params=params)
            if response.status_code == 200:
                result = response.json()
                return jsonify(result), 200
            else:
                return (
                    jsonify(
                        {
                            "error": f"Error calling the intent classification model: {response.status_code}"
                        }
                    ),
                    500,
                )

        except requests.RequestException as e:
            return (
                jsonify(
                    {
                        "error": f"Error calling the intent classification model: {str(e)}"
                    }
                ),
                500,
            )


@app.route("/test-recognition", methods=["GET"])
def test_recognition():
    if request.method == "GET":
        model_endpoint = os.getenv("RECOGNIZER_MODEL_ENDPOINT")

        try:
            response = requests.get(model_endpoint)
            if response.status_code == 200:
                result = response.json()
                return jsonify(result), 200
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
                jsonify(
                    {"error": f"Error calling the gesture recognition model: {str(e)}"}
                ),
                500,
            )


"""
POST /recognize
Recognizes gestures from a given image.

Parameters:
- image (file): The image file to recognize gestures from.

Responses:
- 200 OK: Returns the recognition result from the gesture recognition model.
- 400 Bad Request: Returns an error message if the 'image' parameter is missing.
- 500 Internal Server Error: Returns an error message if there's an error calling the gesture recognition model.

"""


@app.route("/recognize", methods=["POST"])
def recognize():
    if request.method == "POST":
        model_endpoint = (
            os.getenv("RECOGNIZER_MODEL_ENDPOINT") + "/gesture-recognizer/process-image"
        )

        print("RECOGNIZER_MODEL_ENDPOINT:", os.getenv("RECOGNIZER_MODEL_ENDPOINT"))

        file = request.files["file"]

        if not file:
            return jsonify({"error": "Missing 'image' parameter"}), 400

        files = {"file": file}

        try:
            response = requests.post(model_endpoint, files=files)
            if response.status_code == 200:
                result = response.json()
                return jsonify(result), 200
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
                jsonify(
                    {"error": f"Error calling the gesture recognition model: {str(e)}"}
                ),
                500,
            )


if __name__ == "__main__":
    socketio.run(app, debug=True)
