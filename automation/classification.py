def select_data_by_intent(intents):

    url_mapping = {
        "Resource page": "resource-categories",
        "Therapy Support": "resource-categories/therapy",
        "Tech support": "resource-categories/help-with-technology",
        "Emotion support": "resource-categories/emotions-and-social-life",
        "Home page": "home",
    }

    result = {}

    for i in range(len(intents)):
        intent = intents[i]
        result[intent] = url_mapping[intent]

    return result