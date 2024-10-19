import sqlite3

def reset_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS messages')
    c.execute('CREATE TABLE messages (id INTEGER PRIMARY KEY, message TEXT, timestamp TEXT)')
    conn.commit()
    conn.close()
    print("Chat log database reset successfully.")

reset_db()
