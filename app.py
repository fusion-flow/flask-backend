# app.py
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/classify", methods=["GET"])
def classify():
    if request.method == "GET":
        model_endpoint = os.getenv("CLASSIFICATION_MODEL_ENDPOINT")

        query = request.args.get("query", "")

        if not query:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        # Specify the parameters for your request
        params = {
            "query": query,
        }

        # Make a request to the intent classification model
        try:
            response = requests.get(model_endpoint, params=params)
            if response.status_code == 200:
                result = response.json()
                return jsonify(result), 200
            else:
                return (
                    jsonify(
                        {
                            "error": f"Error calling the intent classification model: {response.status_code}"
                        }
                    ),
                    500,
                )

        except requests.RequestException as e:
            return (
                jsonify(
                    {
                        "error": f"Error calling the intent classification model: {str(e)}"
                    }
                ),
                500,
            )


if __name__ == "__main__":
    app.run(debug=True)
