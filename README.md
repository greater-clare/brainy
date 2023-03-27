# How to Use Chatbot

## Creating the Environment

To get the environment working, navigate to the repository's directory and use the following shell commands:

`$ python3 -m venv chatbot_env`

`$ source chatbot_env/bin/activate`

`$ pip install -r requirements.txt`

## Training Data

WhatsApp-exported conversation text (no media files -- they must be omitted at the time of exporting) .txt file must be called "chat.txt" and be in the same directory as the other relevant files necessary for the chatbot.

## Running Chatbot

Again, ensure that the current working directory is the same as the repository, and use the shell command `$ python chatbot.py` The output from this command should be the following:

```
[nltk_data] Downloading package averaged_perceptron_tagger to
[nltk_data]     /Users/kmaurinjones/nltk_data...
[nltk_data]   Package averaged_perceptron_tagger is already up-to-
[nltk_data]       date!
[nltk_data] Downloading package punkt to
[nltk_data]     /Users/kmaurinjones/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package stopwords to
[nltk_data]     /Users/kmaurinjones/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
List Trainer: [####################] 100%
> 
```

The last line of the above output, "> " is the chatbot's prompt where you can enter text and begin the conversation. When you would like to exit the conversation, simply type ":q", "quit", or "exit".

## Other

ChatterBot uses the default SQLStorageAdapter and creates a SQLite file database unless you specify a different storage adapter. Note: The main database file is db.sqlite3, while the other two, ending with -wal and -shm, are temporary support files.