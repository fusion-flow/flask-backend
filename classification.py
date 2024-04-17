import os
import requests
from flask import jsonify

client_url = os.getenv("CLIENT_URL")


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


def get_intents(intent_list):
    upper_threshold = 0.7
    lower_threshold = 0.3
    unique_intents = set()
    for i in range(len(intent_list)):
        intent = intent_list[i]["text"].split("-")[1]
        score = intent_list[i]["score"]
        if i <= 0 and (score > upper_threshold):
            return {intent}
        if score < lower_threshold:
            return unique_intents
        unique_intents.add(intent)
    return unique_intents


def select_data_by_intent(intents):

    url_mapping = {
        "Resource page": "resource-categories",
        "Therapy Support": "resource-categories/therapy",
        "Tech support": "resource-categories/help-with-technology",
        "Emotion support": "resource-categories/emotions-and-social-life",
        "Home page": "home",
    }

    return {intent: url_mapping[intent] for intent in intents}
