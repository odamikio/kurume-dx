from flask import Flask, request, render_template, send_from_directory
import sqlite3

app = Flask(__name__)

def get_usernames():
    conn = sqlite3.connect('kurume-dx.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM employees")
    usernames = cur.fetchall()
    conn.close()
    return [name[0] for name in usernames]

def search_users(query):
    conn = sqlite3.connect('kurume-dx.db')
    cur = conn.cursor()

    cur.execute("""
        SELECT check_in.time, check_in.camera 
        FROM employees 
        JOIN check_in ON check_in.card = employees.card 
        WHERE employees.name LIKE ? ORDER BY check_in.time DESC
    """, ('%' + query + '%',))
    
    results = cur.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    usernames = get_usernames()
    return render_template('index.html', usernames=usernames)

@app.route('/submit', methods=['POST'])
def submit():
    query = request.form.get('query') 
    results = search_users(query) 
    return render_template('results.html', query=query, results=results)

@app.route('/camera_files/<filename>')
def download_file(filename):
    return send_from_directory('camera_files', filename, as_attachment=False)

if __name__ == '__main__':
    app.run(host='172.16.24.77', port=5500, debug=True)
