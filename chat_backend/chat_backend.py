from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/messages/*": {"origins": "*"}})

def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/messages', methods=['GET'])
def get_messages():
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT message, timestamp FROM messages ORDER BY id DESC')
        messages = [{"text": row['message'], "timestamp": row['timestamp']} for row in c.fetchall()]
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def add_message():
    message = request.json['message']
    timestamp = datetime.now().strftime('%H:%M')
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('INSERT INTO messages (message, timestamp) VALUES (?, ?)', (message, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
