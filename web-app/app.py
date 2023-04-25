from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from datetime import datetime
import openai
import os

### VARIABLES

INITIAL_MESSAGE = "Hi! I'm Brainy, a virtual assistant who can guide you through the mental health screening process. Can you start by telling me a bit about the problems you are experiencing?"

#### SET UP ENVIRONMENT
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

users = {}
message_history = {}

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

### UTILITY FUNCTIONS

def clean_users(users=users, message_history=message_history):
    #TODO: Write a function that looks through the connection times in 
    # users, and then removes all records older than a day from both
    # users and message_history
    pass

### INIT WEB APP

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route('/get_initial', methods=['GET'])
def get_initial():
    response = INITIAL_MESSAGE
    
    connect_time = datetime.now()
    user_id = str(hash(connect_time))
    
    users[user_id] = (connect_time)
    message_history[user_id] = [INITIAL_MESSAGE]

    clean_users() # Remove old user IDs and messages from our system
    
    return jsonify({"response": response, "user_id":user_id})

@app.route('/reset_cookie', methods=['GET'])
def reset_cookie():
    # Set cookie value to an empty string
    resp = make_response("Cookie reset")
    resp.set_cookie('last_index', '', expires=datetime.now() - timedelta(days=1))
    return resp

@app.route('/get_response', methods=['GET'])
def get_response():
    message = request.args.get("message")
    user_id = request.args.get("user_id")
    
    response = generate_response(message)
    
    message_history[user_id].extend([message, response])
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run()
