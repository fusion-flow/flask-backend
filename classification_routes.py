# from flask import Blueprint, jsonify, request
# from classification import perform_classification

# classification_bp = Blueprint("classification", __name__)


# @classification_bp.route("/classify", methods=["GET"])
# def classify():
#     print("classify")
#     if request.method == "GET":
#         query = request.args.get("query", "")
#         a = perform_classification(query)
#         print(a)
#         return a
