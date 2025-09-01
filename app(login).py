from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        users = load_users()

        if username in users:
            return render_template('error.html', message="⚠️ Username already exists!")
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        users = load_users()

        if username in users and users[username] == password:
            return redirect("https://locked-bool-blond-hostel.trycloudflare.com")
        else:
            return render_template('error.html', message="❌ Invalid username or password.")
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
