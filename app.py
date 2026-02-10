from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample user data
users = {'user': 'password'}
scores = {}
quizzes = {
    "quiz1": [
        {"question": "What is 2 + 2?", "options": ["3", "4", "5"], "answer": "4"},
        {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin"], "answer": "Paris"},
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    user_scores = scores.get(session['username'], {})
    return render_template('dashboard.html', scores=user_scores)

@app.route('/quiz/<quiz_name>', methods=['GET', 'POST'])
def quiz(quiz_name):
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        score = 0
        for question in quizzes[quiz_name]:
            user_answer = request.form.get(question['question'])
            if user_answer == question['answer']:
                score += 1
        scores[session['username']] = scores.get(session['username'], {})
        scores[session['username']][quiz_name] = score
        return redirect('/dashboard')
    return render_template('quiz.html', quiz=quizzes[quiz_name])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)