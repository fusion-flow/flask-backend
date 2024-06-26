import constants

def utter_intro(states):
  return "Hi! I'm Alex. How can I help you today?"

def utter_greet(states):
  return "Hi! I'm here to assist you."

def utter_capability(states):
  return "I can help you to find resources from this website"

def utter_if_right_page(states, intent):
  response = "We have redirected you to " + intent +"</br>Is this the resource you wanted?"
  return response

def utter_happy(states):
  return "Great!!! Let me know if you need anything else."

def handle_deny(states):
  return "Can you please tell me what you want more precisely"

def utter_welcome(states):
  return "You are welcome"

def utter_unavailability(states):
  return "I'm sorry, we don't have requested resource."

def utter_navigation_list(states):
  return "Following are the pages that are related to your request. Please choose what you need."

def utter_goodbye(states):
  return "Good bye! Have a nice day."