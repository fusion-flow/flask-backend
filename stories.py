import actions

stories = {
    "start": actions.utter_intro,
    "greet": actions.utter_greet,
    "ask_capability": actions.utter_capability,
    "navigation": actions.utter_if_right_page,
    "confirm": actions.utter_happy,
    "deny": actions.handle_deny,
    "navigation_list": actions.utter_navigation_list,
    "unavailable_page": actions.utter_unavailability,
    "thank": actions.utter_welcome,
    "goodbye": actions.utter_goodbye
}