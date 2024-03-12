import os
import requests
from flask import jsonify


def transcribe_audio(audio_file):
    model_endpoint = os.getenv("TRANSCRIPTION_MODEL_ENDPOINT") + "/whisper/"
    if not audio_file:
        return jsonify({"error": "Missing audio file for transcription"}), 400

    # Make a request to the intent classification model
    try:
        response = requests.post(model_endpoint, files={"files": audio_file})
        if response.status_code == 200:
            result = response.json()
            print("Transcription result:", result["results"][0]["transcript"])
            return result["results"][0]["transcript"], 200
        else:
            return (
                jsonify(
                    {
                        "error": f"Error calling the transcription model: {response.status_code}"
                    }
                ),
                500,
            )

    except requests.RequestException as e:
        return (
            jsonify({"error": f"Error calling the transcription model: {str(e)}"}),
            500,
        )
