from flask import Flask, request, jsonify, make_response
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from conv_cleaner import clean_corpus
from flask_cors import CORS
import json
import numpy as np
import pandas as pd
import re
import os
import openai
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
from time import sleep
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

CORPUS_FILE = "chat.txt"

chatbot = ChatBot("Fambot")

trainer = ListTrainer(chatbot)
cleaned_corpus = clean_corpus(CORPUS_FILE)
trainer.train(cleaned_corpus)

app = Flask(__name__)
CORS(app)

# load questions as json data
def json_loader(folder, filename):
    with open(folder+filename) as fh:
        file = json.load(fh)
    return file

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route('/get_initial', methods=['GET'])
def get_initial():
    response = str("Hi! I am an online assistive agent who will guide you through the Depression Questionnaire! Please note that I am not a replacement for a therapist!")
    return jsonify({"response": response})

@app.route('/reset_cookie', methods=['GET'])
def reset_cookie():
    # Set cookie value to an empty string
    resp = make_response("Cookie reset")
    resp.set_cookie('last_index', '', expires=datetime.now() - timedelta(days=1))
    return resp
responses = [
    "Hello Anne, it's a pleasure to meet you. What brings you in today? Are you looking for help with any particular issue or just hoping to talk things out?",
    "I'm here to listen, Anne. Can you help me understand a little more about how things have been going for you lately? On a scale of 0-4, where 0 is not at all and 4 is nearly every day, how often have you been bothered by having little interest or pleasure in doing things?",
    "Thanks for sharing that, Anne. How long have you been feeling this way? Have you experienced any significant life events or changes recently that may have triggered these emotions?",
    "Thank you for letting me know. How often do you experience these mood swings?",
    "I see. How about your appetite? How often have you been bothered by having a poor appetite or overeating?",
    "That can definitely affect your energy levels and mood. Speaking of mood, would you say you experience any irritability, restlessness, or anxiety?",
    "Thank you for sharing that with me. It takes strength to confront emotions and feelings like these. The good news is that we can work through them together. Based on what you've shared so far, it sounds like you may be experiencing some symptoms of depression. How would you feel about discussing this further?",
    "Alright, have you experienced any concentration difficulties lately?",
    "Based on your answers, it seems like you are experiencing several symptoms related to low mood, low energy, poor appetite, feelings of guilt, difficulty concentrating or being restless. All of these put together indicate that you might be going through depression. It would be beneficial to seek professional help to confirm the diagnosis and receive effective treatment. Would you like me to help you find a mental health professional in your area?"
]

index = 0  # Initialize the index

@app.route('/get_response', methods=['GET'])
def get_response():
    global index  # Use the global index variable

    # Check if we have sent all responses
    if index >= len(responses):
        response = "Sorry, I have no more responses."
    else:
        # Get the response for the current index
        response = responses[index]
        index += 1  # Increment the index
    delay = random.uniform(1.5, 3)
    sleep(delay)
    return jsonify({"response": response})



if __name__ == '__main__':
    app.run(debug=True)
