def fuse_intents(text_intents, audio_intents):

    if audio_intents:
        combined_intents = text_intents + audio_intents
    else:
        combined_intents = text_intents

    combined_intents = sorted(combined_intents, key=lambda x: x["score"], reverse=True)

    unique_intents = identify_intents(combined_intents)
    return unique_intents

def identify_intents(intent_list):
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