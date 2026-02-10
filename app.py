import json
from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load questions from questions.json
with open('questions.json') as f:
    questions = json.load(f)

# Sample user data for PIN login
users = {"user1": "1234", "user2": "5678"}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    pin = request.form['pin']
    user = request.form['username']
    if user in users and users[user] == pin:
        session['user'] = user
        return redirect(url_for('dashboard'))
    return "Invalid PIN! Try again."

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', user=session['user'], questions=questions)

@app.route('/quiz')
def quiz():
    if 'user' not in session:
        return redirect(url_for('home'))
    # Quiz implementation goes here
    return render_template('quiz.html', questions=questions)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)