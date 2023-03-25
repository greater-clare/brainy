# How to Use Chatbot

## Running Chatbot

To run the chatbot, navigate to the directory of the `chatbot.py` file, and use the shell command `$ python chatbot.py`

## Training Data

Whatsapp-exported conversation text (no media files -- they must be omitted at the time of exporting) .txt file must be called "chat.txt" and be in the same directory as the other relevant files necessary for the chatbot.

## Other

ChatterBot uses the default SQLStorageAdapter and creates a SQLite file database unless you specify a different storage adapter. Note: The main database file is db.sqlite3, while the other two, ending with -wal and -shm, are temporary support files.