from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('kurume-dx.db')

@app.route('/insert_temp_data', methods=['POST'])
def insert_temp_data():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperature (time, temp) VALUES (?, ?)", (data['time'], data['temp']))
    conn.commit()
    conn.close()
    return 'Temperature data inserted', 200

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temperature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            temp REAL NOT NULL
        )
    ''')    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='172.16.24.77', port=6500)