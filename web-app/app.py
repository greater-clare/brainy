from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import openai
import os

#### SET UP ENVIRONMENT
openai.api_key = os.getenv("OPENAI_API_KEY")
counter = 0

app = Flask(__name__)
CORS(app)

### RESPONSE FUNCTIONS

def generate_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text.strip()
    return message

### INIT WEB APP

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route('/get_initial', methods=['GET'])
def get_initial():
    response = "Hi! I'm Brainy, a virtual assistant who can guide you through the mental health screening process. Can you start by telling me a bit about the problems you are experiencing?"
    return jsonify({"response": response})

@app.route('/reset_cookie', methods=['GET'])
def reset_cookie():
    # Set cookie value to an empty string
    resp = make_response("Cookie reset")
    resp.set_cookie('last_index', '', expires=datetime.now() - timedelta(days=1))
    return resp

@app.route('/get_response', methods=['GET'])
def get_response():
    message = request.args.get("message")
    response = generate_response(message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
