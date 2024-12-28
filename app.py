from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from pymongo import MongoClient
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']
users = db['users']

# Path to the public directory
PUBLIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public')

@app.route('/')
def home():
    if 'email' in session:
        return render_template('index.html')
    return redirect(url_for('signin'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        existing_user = users.find_one({"email": request.form['email']})

        if existing_user is None:
            if request.form['password'] == request.form['confirm_password']:
                hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                users.insert_one({
                    'username': request.form['username'],
                    'email': request.form['email'],
                    'password': hashpass,
                    'fullname': request.form['fullname']
                })
                session['email'] = request.form['email']
                return redirect(url_for('home'))
            else:
                return 'Passwords do not match!'
        return 'That email already exists!'

    return send_from_directory(PUBLIC_DIR, 'signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['email'] = login_user['email']
                return redirect(url_for('home'))
            return 'Invalid username/password combination'

    return send_from_directory(PUBLIC_DIR, 'signin.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('signin'))

# Serve static files (like CSS and JS)
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory(PUBLIC_DIR, path)

if __name__ == '__main__':
    app.run(debug=True)
