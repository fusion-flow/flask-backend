from flask import session
import constants

def fuse_intents(text_intents, audio_intents, gesture_intent=None):
    print("===========",text_intents, audio_intents)
    print("gesture_intent", gesture_intent)
    combined_intents = text_intents + audio_intents

    combined_intents = sorted(combined_intents, key=lambda x: x["score"], reverse=True)

    unique_intents = identify_intents(combined_intents)

    if gesture_intent and (unique_intents[0]['score'] < gesture_intent['score']):
        unique_intents = [gesture_intent]

    if len(unique_intents) > 1:
        session['state'] = constants.NAVIGATION_LIST_STATE
    else:
        if session['state'] == constants.NAVIGATION_LIST_STATE:
            session['state'] = constants.NORMAL_STATE
    
    print("unique_intents", unique_intents)

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