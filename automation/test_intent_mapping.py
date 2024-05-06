from classification import select_data_by_intent

def test_single_intent():
    intents = ["Home page"]
    expected_output = {"Home page": "home"}
    assert select_data_by_intent(intents) == expected_output

def test_multiple_intents():
    intents = ["Therapy Support", "Tech support", "Emotion support"]
    expected_output = {
        "Therapy Support": "resource-categories/therapy",
        "Tech support": "resource-categories/help-with-technology",
        "Emotion support": "resource-categories/emotions-and-social-life"
    }
    assert select_data_by_intent(intents) == expected_output

def test_empty_list():
    intents = []
    expected_output = {}
    assert select_data_by_intent(intents) == expected_output

def test_unknown_intent():
    intents = ["Unknown"]
    try:
        select_data_by_intent(intents)
    except KeyError:
        assert True
    else:
        assert False, "Expected KeyError but no exception was raised."

def test_duplicate_intents():
    intents = ["Home page", "Home page", "Home page"]
    expected_output = {"Home page": "home"}
    assert select_data_by_intent(intents) == expected_output

