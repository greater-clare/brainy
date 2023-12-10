from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json
import os

print("Imports complete")

# Helper functions for importing files
def loader(function, path:str, folder:str=""):
    # Check folder is formatted correctly
    if folder and folder[-1] != "/": folder+="/"
    # Read the file
    try:
        with open(folder+path, "r") as f:
            data = function(f)
        return data
    except FileNotFoundError:
        print(f"ERROR: {folder+path} does not exist!")

def txt_loader(path:str, folder:str="") -> str:
    return loader(lambda f: f.read(), path, folder)  

def json_loader(path:str, folder:str="") -> dict:
    return loader(lambda f: json.load(f), path, folder)      

print("Base functions created")

# Load config
config_path = "config.json"
config = json_loader(config_path)
openai_key = txt_loader(config["path"]["openai-key"])

print("Config loaded")

# Connect to LLM and test connection
llm = ChatOpenAI(openai_api_key=openai_key, temperature=config["temperature"], model=config["model"])
try: #TODO make error checking more robust here.
    llm(messages=[HumanMessage(content="Hello world")])
except Exception as e:
    print("LLM connection failed.")
    raise(e)

print("LLM connected")

# Load questionnaires and assess available topics
questionnaire_loader = lambda filename: json_loader(filename, config["path"]["questionnaires"])

questionnaire_index = questionnaire_loader("index.json")
questionnaire_topics = ", ".join(questionnaire_index.keys())

print(f"Found questionaires for {questionnaire_topics}")

# Session class
class Session():
    def __init__(self) -> None:
        self.state = "initial"
        self.system = SystemMessagePromptTemplate.from_template(config["prompts"][self.state]).format(topics=questionnaire_topics)
        self.opening_message = AIMessage(content=config["prompts"]["opening_message"])
        self.messsages = [self.system, self.opening_message]
        self.scores = {}

    def add_messages(self, *messages) -> None:
        self.messsages.extend(messages)

print("Loaded Brainy")

# Interactive mode
if __name__ == "__main__":
    print("\nStarting interactive mode...")
    os.system("cls||clear")
    
    session = Session()
    print(session.opening_message.content)

    while True:
        userMessage = HumanMessage(content=input("> "))
        
        # TODO: improve error handling
        if not userMessage:
            print("ERROR: Not a valid input")
            continue

        response = llm(messages=session.messsages+[userMessage])
        print(response.content)
        session.add_messages(userMessage, response)

