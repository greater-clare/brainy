# chatbot.py

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from conv_cleaner import clean_corpus

CORPUS_FILE = "chat.txt"

chatbot = ChatBot("Fambot")

trainer = ListTrainer(chatbot)
cleaned_corpus = clean_corpus(CORPUS_FILE)
trainer.train(cleaned_corpus)

exit_conditions = [":q", "quit", "exit"]
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"{chatbot.get_response(query)}")