from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'
questions = []

# Load questions from JSON file
def load_questions():
    global questions
    with open('questions.json') as f:
        questions = json.load(f)

load_questions()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    pin = request.form['pin']
    # Simple validation
    if pin.isdigit() and len(pin) == 4:
        session['name'] = name
        session['pin'] = pin
        session['attempts'] = 0
        session['correct_answers'] = 0
        session['quizzes'] = []
        return redirect(url_for('dashboard'))
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', 
                           name=session['name'],
                           attempts=session['attempts'],
                           correct_answers=session['correct_answers'],
                           accuracy=(session['correct_answers'] / session['attempts'] * 100) if session['attempts'] > 0 else 0)

@app.route('/quiz/<int:num_questions>')
def quiz(num_questions):
    selected_questions = random.sample(questions, k=num_questions)
    return render_template('quiz.html', questions=selected_questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    correct_count = 0
    quiz_answers = request.form.getlist('answers[]')
    for question, answer in zip(questions, quiz_answers):
        if question['answer'] == answer:
            correct_count += 1
    session['attempts'] += 1
    session['correct_answers'] += correct_count
    session['quizzes'].append({
        'attempt': session['attempts'],
        'correct': correct_count
    })
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
