Keylogger Project
This project implements a Python-based keylogger client and a Flask server to capture, process, and store keystrokes as words. The keylogger buffers keystrokes, processes them into words (handling backspaces and special keys), and saves them locally in JSON and text formats while sending them to a Flask server for further processing and storage.
⚠️ Warning: This project is for educational purposes only. Unauthorized keylogging is illegal and unethical. Ensure you have explicit permission from users before deploying.
Features

Keylogger Client (keylogger.py):
Captures keystrokes using the pynput library and buffers them until a word boundary (space, enter, tab) or timeout (5 seconds).
Processes keystrokes to handle backspaces and special keys, forming complete words.
Saves words with timestamps to logs.json in JSON format.
Appends words to log.txt with spaces between them.
Sends each word to the Flask server at http://localhost:5000/log.
Stops on Esc key press.


Flask Server (server.py):
Receives words via POST requests to /log.
Processes received keystrokes to reconstruct words, handling backspaces and special key markers.
Stores up to 1000 entries in memory (volatile) with timestamps, raw keys, and processed words.
Provides a GET endpoint (/get-data) to retrieve stored data in summary or raw format.



Prerequisites

Python 3.6+
Dependencies:
Client: pynput, requests
Server: flask


A system with permission to capture keystrokes (may require elevated privileges on Linux/macOS).

Installation

Clone the Repository
git clone https://github.com/your-username/keylogger-project.git
cd keylogger-project


Set Up a Virtual Environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
pip install pynput flask requests


File StructureEnsure the following files are in your project directory:

keylogger.py: The keylogger client.
server.py: The Flask server.



Usage
Running the Flask Server

Start the server:python3 server.py

The server runs on http://0.0.0.0:5000 (accessible at http://localhost:5000).
Test the server:
Send a POST request to /log:curl -X POST http://localhost:5000/log -H "Content-Type: application/json" -d '{"keys": "hello world", "timestamp": "2025-08-01T23:41:00.000Z"}'

Expected response:{
  "status": "success",
  "words_received": 2,
  "storage_count": 1
}


Retrieve data with a GET request:curl http://localhost:5000/get-data

Or for raw data:curl http://localhost:5000/get-data?format=raw





Running the Keylogger Client

Ensure the server is running (optional if you only want local logging).
Run the client:python3 keylogger.py

On Linux/macOS, you may need:sudo python3 keylogger.py


The client will:
Capture keystrokes and buffer them into words (split on space, enter, tab, or after 5 seconds).
Save words to logs.json (with timestamps and "Word" action).
Append words to log.txt (with spaces between).
Send each word to the server.
Print: [+] Running Keylogger Successfully! [!] Saving words in 'logs.json' and 'log.txt'.


Stop the keylogger by pressing Esc.

Example Output

Typing: hello world<space>how<enter>are<tab>you
logs.json:[
    {
        "Timestamp": "2025-08-01 23:41:00",
        "Action": "Word",
        "Key": "hello"
    },
    {
        "Timestamp": "2025-08-01 23:41:01",
        "Action": "Word",
        "Key": "[SPACE]"
    },
    {
        "Timestamp": "2025-08-01 23:41:02",
        "Action": "Word",
        "Key": "world"
    },
    ...
]


log.txt:hello [SPACE] world [SPACE] how [ENTER] are [TAB] you


Server Storage (via curl http://localhost:5000/get-data?format=raw):{
    "entries": [
        {
            "timestamp": "2025-08-01T23:41:00.123456",
            "raw_keys": "hello",
            "words": ["hello"]
        },
        {
            "timestamp": "2025-08-01T23:41:01.123456",
            "raw_keys": "[SPACE]",
            "words": []
        },
        ...
    ]
}



Security Considerations

Keylogger: Captures sensitive data. Use only with explicit user consent and in compliance with local laws.
Server: The /get-data endpoint lacks authentication. For production, add API keys or JWT authentication.
Network: Use HTTPS for server communication in production to protect keylogs.
Storage: The server stores data in memory (lost on restart). For persistence, modify to use a file or database.

Limitations

The keylogger may require elevated permissions (sudo) on Linux/macOS to capture certain keys.
Server storage is in-memory and volatile. Consider SQLite or file storage for persistence.
The client sends each word individually, which may generate many requests. Modify to batch words for efficiency if needed.

Production Deployment

Server: Use a WSGI server like Gunicorn:pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app

Set up a reverse proxy (e.g., Nginx) and HTTPS for security.
Client: Ensure it runs with appropriate permissions and error handling for server communication.
Persistence: Modify server.py to save to a file or database for persistent storage.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is for educational purposes only and is not licensed for commercial use. Use responsibly and ethically.
