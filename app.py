from flask import Flask, render_template
from flask import request as req
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    input_text = req.form.get("inputText")
    summarized_text = perform_summarization(input_text)
    return render_template("index.html", summary=summarized_text["summary_text"])


def perform_summarization(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "[API TOKEN]"} # Give you API Token here

    data = req.form["inputText"]
    minL = 150
    maxL = int(req.form.get("summaryLength"))

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query(
        {
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        }
    )[0]

    return output


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
