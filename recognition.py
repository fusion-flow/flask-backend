import os
import requests
from flask import jsonify, request

model_endpoint = (
    os.getenv("RECOGNIZER_MODEL_ENDPOINT") + "/gesture-recognizer/process-image"
)
print("RECOGNIZER_MODEL_ENDPOINT:", os.getenv("RECOGNIZER_MODEL_ENDPOINT"))


def perform_recognition(query):

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
