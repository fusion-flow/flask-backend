import requests
from flask import jsonify
from fusion import fuse_intents
from flask_socketio import emit
import os

def handle_audio_message(message):
    
    text_message = message["message"]
    audio_blob = message["audio"]
    audio_intents, text_intents= [], []
    transcribed_text, status_code = transcribe_audio(audio_blob)
    if transcribed_text:
        audio_intents = perform_classification(transcribed_text)
    if text_message:
        text_intents = perform_classification(text_message)


    fused_intents = fuse_intents(text_intents, audio_intents)
    emit("audio_message", fused_intents)

def perform_classification(query):
    model_endpoint = os.getenv("CLASSIFICATION_MODEL_ENDPOINT") + "/search"
    print("CLASSIFICATION_MODEL_ENDPOINT:", os.getenv("CLASSIFICATION_MODEL_ENDPOINT"))

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

            return result
            #     print("result", result)
            #     intents = list(get_intents(result))
            #     # print("intents", intents)
            #     urls = select_data_by_intent(intents)

            # print(urls)
            # for key, value in urls.items():
            #     urls[key] = client_url + value
            # return urls
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
                {"error": f"Error calling the intent classification model: {str(e)}"}
            ),
            500,
        )
    
def transcribe_audio(audio_file):
    model_endpoint = os.getenv("TRANSCRIPTION_MODEL_ENDPOINT") + "/whisper/"
    if not audio_file:
        return jsonify({"error": "Missing audio file for transcription"}), 400

    # Make a request to the intent classification model
    try:
        response = requests.post(model_endpoint, files={"files": audio_file})
        if response.status_code == 200:
            result = response.json()
            # print("Transcription result:", result["results"][0]["transcript"])
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
    
def fuse_intents(text_intents, audio_intents, gesture_intent=None):
    # print("===========",text_intents, audio_intents)
    # print("gesture_intent", gesture_intent)
    combined_intents = text_intents + audio_intents

    combined_intents = sorted(combined_intents, key=lambda x: x["score"], reverse=True)

    unique_intents = identify_intents(combined_intents)

    if gesture_intent and (unique_intents[0]['score'] < gesture_intent['score']):
        unique_intents = [gesture_intent]

    # if len(unique_intents) > 1:
    #     session['state'] = constants.NAVIGATION_LIST_STATE
    # else:
    #     if session['state'] == constants.NAVIGATION_LIST_STATE:
    #         session['state'] = constants.NORMAL_STATE
    
    # print("unique_intents", unique_intents)

    return unique_intents

def identify_intents(intent_list):
    upper_threshold = 0.7
    lower_threshold = 0.3
    unique_intents = []
    for i in range(len(intent_list)):
        intent = intent_list[i]["text"].split("-")[1]
        score = intent_list[i]["score"]
        if i <= 0 and (score > upper_threshold):
            return [intent]
        if score < lower_threshold:
            return unique_intents
        if intent not in unique_intents:
            unique_intents.append(intent)
    return unique_intents