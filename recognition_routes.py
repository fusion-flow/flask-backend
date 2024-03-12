# import os
# import requests
# from flask import jsonify, request
# from flask import Blueprint
# from recognition import perform_recognition


# recognition_bp = Blueprint("recognition", __name__)

# """
# POST /recognize
# Recognizes gestures from a given image.

# Parameters:
# - image (file): The image file to recognize gestures from.

# Responses:
# - 200 OK: Returns the recognition result from the gesture recognition model.
# - 400 Bad Request: Returns an error message if the 'image' parameter is missing.
# - 500 Internal Server Error: Returns an error message if there's an error calling the gesture recognition model.

# """


# @recognition_bp.route("/recognize", methods=["POST"])
# def recognize():
#     if request.method == "POST":
#         return perform_recognition()
