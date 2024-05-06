from fusion import identify_intents, fuse_intents

def test_empty_intent_list():
  """Test with an empty intent list."""
  intent_list = []
  assert identify_intents(intent_list) == []

def test_no_above_threshold():
  """Test with no intent above the lower threshold."""
  intent_list = [
    {"text": "I want to go to home page-Home page", "score": 0.1},
    {"text": "Please take me to the home page-Home page", "score": 0.2},
    {"text": "Can I get information about therapy?-Therapy Support", "score": 0.15},
    {"text": "I want to get tech support-Tech support", "score": 0.11}
    ]
  assert identify_intents(intent_list) == []

def test_single_intent_above_upper_threshold():
  """Test with a single intent above the upper threshold."""
  intent_list = [
    {"text": "I want to go to home page-Home page", "score": 0.9},
    {"text": "Please take me to the home page-Home page", "score": 0.2},
    {"text": "Can I get information about therapy?-Therapy Support", "score": 0.15},
    {"text": "I want to get tech support-Tech support", "score": 0.11}
    ]
  assert identify_intents(intent_list) == ["Home page"]

def test_multiple_intent_above_threshold():
  """Test with a single intent above the upper threshold."""
  intent_list = [
    {"text": "I want to go to home page-Home page", "score": 0.66},
    {"text": "Please take me to the home page-Home page", "score": 0.55},
    {"text": "Can I get information about therapy?-Therapy Support", "score": 0.44},
    {"text": "I want to get tech support-Tech support", "score": 0.59}
    ]
  assert identify_intents(intent_list) == ["Home page","Therapy Support", "Tech support"]

def test_multiple_intent_threshold():
  """Test with a single intent above the upper threshold."""
  intent_list = [
    {"text": "I want to go to home page-Home page", "score": 0.66},
    {"text": "Please take me to the home page-Home page", "score": 0.55},
    {"text": "Can I get information about therapy?-Therapy Support", "score": 0.15},
    {"text": "I want to get tech support-Tech support", "score": 0.11}
    ]
  assert identify_intents(intent_list) == ["Home page"]

def test_fuse_intents():
  """Test the fusion of intents."""
  text_intents = [
    {"text": "I want to go to home page-Home page", "score": 0.1},
    {"text": "Please take me to the home page-Home page", "score": 0.2},
    {"text": "Can I get information about therapy?-Therapy Support", "score": 0.15},
    {"text": "I want to get tech support-Tech support", "score": 0.11}
    ]
  audio_intents = [
    {"text": "take me to the main page-Home page", "score": 0.66},
    {"text": "I need home page-Home page", "score": 0.55},
    {"text": "Direct me to the home-Home page", "score": 0.15}
  ]
  assert fuse_intents(text_intents, audio_intents) == ["Home page"]

def test_fuse_audio_intents():
  """Test the fusion of intents."""
  text_intents = []
  audio_intents = [
    {"text": "take me to the main page-Home page", "score": 0.66},
    {"text": "I need home page-Home page", "score": 0.55},
    {"text": "Direct me to the home-Home page", "score": 0.15}
  ]
  assert fuse_intents(text_intents, audio_intents) == ["Home page"]

def test_fuse_text_intents():
  """Test the fusion of intents."""
  text_intents = [
    {"text": "take me to the main page-Home page", "score": 0.66},
    {"text": "I need home page-Home page", "score": 0.55},
    {"text": "Direct me to the home-Home page", "score": 0.15}
  ]
  audio_intents = []
  assert fuse_intents(text_intents, audio_intents) == ["Home page"]

def test_fuse_no_intents():
  """Test the fusion of intents."""
  text_intents = []
  audio_intents = []
  assert fuse_intents(text_intents, audio_intents) == []
