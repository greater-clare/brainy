# chatbot.py

# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
import os
# from chatbot_diagnostics import *

questionnaire_loader = lambda name: json_loader("questionnaires/", name)
index = questionnaire_loader("index.json")

# training data is stored in an sqlite3 file, but we don't want user-inputted data to be stored across multiple sessions
# this makes sure the training data is reset every time the bot is loaded - so it doesn't use past data
# os.remove("db.sqlite3")

# CORPUS_FILE = [] # list of supportive responses
# with open("data/bot_responses.txt", "r") as file:
#     for line in file.read().split("\n"):
#         CORPUS_FILE.append(line.strip())

# chatbot = ChatBot("Brainy", read_only = True)
# chatbot.storage.drop()

# trainer = ListTrainer(chatbot)
# trainer.train(CORPUS_FILE)

# exit_conditions = [":q", "quit", "exit"]

# questionnaires = [PHQ9(filename = "phq-9.json"), GAD7(filename="gad-7.json"), ASRS5(filename="asrs-5.json"),
#                   ZFOCS(filename="zf-ocs.json"), PCPTSD(filename="pc-ptsd.json", cut_point=4)]

# questionnaires = [PHQ9(filename = "phq-9.json")]
print ("\nHello, I am a chatbot.")

PHQ9(filename = "phq-9.json")
# GAD7(filename = "gad-7.json")
# ASRS5(filename="asrs-5.json")
# ZFOCS(filename="zf-ocs.json")
# PCPTSD(filename="pc-ptsd.json", cut_point=4)

# while True:
#     # for quest in questionnaires:
#     #     # query = input(f"\n{quest}: ")
#     #     query = input(f"\n{quest}\n")
#     #     if query in exit_conditions:
#     #         break
#     #     break
#     # query = input(f"\nklajshdfls: \n")
#     # if query in exit_conditions:
#         # break
#         # else:
#             # print(f"Brainy: {chatbot.get_response(query)}\n")
#     print ("\nThank you for your responses.")
#     break

print ("\nThank you for your responses.")

# general support services to recommend after survey is complete
try:
    print("\nIf you are in need of immediate support, please consider services like the following:\n")
    with open("data/services.txt", "r") as file:
        for line in file.read().split("\n"):
            print(line.strip())
except:
    FileNotFoundError
    # break
