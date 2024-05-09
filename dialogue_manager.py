from data import keyword_intent, intent_url
import constants
from flask import session
from stories import stories
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

# stop_words = set(stopwords.words('english'))

# def remove_stopwords(sentence):
        
#     word_tokens = word_tokenize(sentence)
#     filtered_words = [w for w in word_tokens if not w.lower() in stop_words]
#     filtered_sentence = ' '.join(filtered_words)
    
#     return filtered_sentence



def generate_response(fused_intents):

    # set states session variable if it does not exists
    if "states" in session:
        states = session["states"]
    else:
        session["states"] = []
        states = session["states"]

    intent_url_mapping = {}
    

    # unavailable page
    if len(fused_intents) == 0:
        response = stories["unavailable_page"](states)
        intent = "unavailable_page"
        session["state"] = constants.UNAVAILABLE
    # direct navigation 
    elif session["state"] != constants.NAVIGATION_LIST_STATE and len(fused_intents) == 1:
        intent = fused_intents[0]
        intent_url_mapping = get_urls(fused_intents)

        if intent not in stories:
            response = stories["navigation"](states, intent)
            session["state"] = constants.DIRECT_NAVIGATION
        else:
            response = stories[intent](states)
    # list    
    # if session["state"] == constants.NAVIGATION_LIST_STATE and fused_intents:
    else:
        states = session["states"]
        response = stories["navigation_list"](states)
        intent = "navigation_list"
        other_intents = []

        # remove unnessary intents from the list
        ## WHAT HAPPEN WHEN THE FIRST ELEMENT IS INTENT IN STORIES ?
        i = 0
        num_fuesd_intents = len(fused_intents)
        while i < num_fuesd_intents:
            if fused_intents[i] in stories:
                other_intents.append(fused_intents.pop(i))
                num_fuesd_intents -= 1
            else:
                i += 1
        
        # get only first five intents
        fused_intents = fused_intents[:5]

        if fused_intents:
            # get intent to url mapping result
            intent_url_mapping = get_urls(fused_intents)
            session["state"] = constants.NAVIGATION_LIST_STATE
            session["states"].append(constants.NAVIGATION_LIST_STATE)
        else:
            # all intents are other intents
            intent = other_intents[0]
            response = stories[intent](states)
            session["state"] = constants.NORMAL_STATE

    # check if state is denied
    if intent == "deny":
        session["state"] = constants.DENIED
        session["states"].append(constants.DENIED)
    elif intent != "navigation_list":
        session["states"].append(session["state"])

    print("states in generate response", session["states"])

    return response, intent_url_mapping


def get_urls(intents):
    intent_url_mapping = {}
    url_list = []

    # iterate intents and map with url
    for i in range(len(intents)):
        intent = intents[i]

        # check if intent exist in intent_url dictionary
        if intent not in intent_url:
            continue
        
        url = intent_url[intent]
        intent_url_mapping[intent] = url
        url_list.append([url, intent])
    
    session["intent_list"] = url_list

    return intent_url_mapping