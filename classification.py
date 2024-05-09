import os
import requests
from flask import jsonify
from data import keyword_intent

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


def get_intents(keywords_scores):

    # iterate keywords and scores and map with intent
    for i in range(len(keywords_scores)):

        keyword = keywords_scores[i]["text"]

        # check if keyword exist in keyword_intent dictionary
        if keyword not in keyword_intent:
            keyword_intent.pop(i) # remove non existing keywords from the keyword_intent list
            continue
        
        intent = keyword_intent[keyword]

        keywords_scores[i]["intent"] = intent

    return keywords_scores


def select_data_by_intent(intents):

    url_mapping = {
        "Resource page": "resource-categories",
        "Therapy Support": "resource-categories/therapy",
        "Tech support": "resource-categories/help-with-technology",
        "Emotion support": "resource-categories/emotions-and-social-life",
        "Home page": "home",
    }

    return {intent: url_mapping[intent] for intent in intents}
