from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = './camera_files'

def connect_db():
    return sqlite3.connect('kurume-dx.db')

@app.route('/insert_card_data', methods=['POST'])
def insert_card_data():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO check_in (time, card, camera) VALUES (?, ?, ?)", (data['time'], data['card'], data['camera']))
    conn.commit()
    conn.close()
    return 'Card data inserted', 200

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
        CREATE TABLE IF NOT EXISTS check_in (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            card TEXT NOT NULL,
            camera TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temperature (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            temp REAL NOT NULL
        )
    ''')    
    conn.commit()
    conn.close()

@app.route('/upload-image', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    print(file_path)
    file.save(file_path)
    
    return f"File {file.filename} uploaded successfully", 200

if __name__ == '__main__':
    init_db()
    app.run(host='172.16.24.77', port=6500)
