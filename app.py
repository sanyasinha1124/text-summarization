from flask import Flask,render_template, request, jsonify
from transformers import pipeline

# Initialize Flask app and the summarizer
app = Flask(__name__)
summarizer = pipeline("summarization")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
    

@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Please provide input text in JSON format with a 'text' field."}), 400

    input_text = data["text"]

    if len(input_text.strip()) < 20:
        return jsonify({"error": "Input text is too short to summarize."}), 400

    try:
        result = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
        summary = result[0]['summary_text']
        return jsonify({"summary": summary}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

import requests

url = "http://127.0.0.1:5000/summarize"
data = {"text": "Your long text here that needs to be summarized."}

response = requests.post(url, json=data)
print(response.json())

