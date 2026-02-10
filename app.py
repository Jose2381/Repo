from flask import Flask, render_template_string, request, redirect, session, flash
import json
import random
import time

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Change to a random secret key

# Sample in-memory data for user sessions
users = {
    'user1': '1234',  # Example user and PIN
}

# Load questions from a JSON file
def load_questions():
    with open('questions.json') as f:
        return json.load(f)

questions = load_questions()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pin = request.form.get('pin')
        if pin in users.values():
            session['authenticated'] = True
            session['score'] = 0
            session['answers'] = []
            return redirect('/quiz')
        else:
            flash('Invalid PIN. Please try again.')
    return render_template_string('''
        <h1>Login</h1>
        <form method="post">
            <input type="password" name="pin" placeholder="Enter your PIN" required>
            <button type="submit">Login</button>
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
    ''')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'authenticated' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        question_id = int(request.form.get('question_id'))
        selected_answer = request.form.get('answer')
        correct_answer = questions[question_id]['answer']

        # Update score and answers
        if selected_answer == correct_answer:
            session['score'] += 1
        session['answers'].append((questions[question_id]['question'], selected_answer, correct_answer))

        # Move to the next question or show results
        if question_id + 1 < len(questions):
            return redirect(f'/quiz/{question_id + 1}')
        else:
            return redirect('/results')

    question_id = int(request.args.get('question_id', 0))
    question = questions[question_id]
    return render_template_string('''
        <h1>Quiz</h1>
        <h2>{{ question.question }}</h2>
        <form method="post">
            {% for answer in question.answers %}
                <input type="radio" id="{{ answer }}" name="answer" value="{{ answer }}" required>
                <label for="{{ answer }}">{{ answer }}</label><br>
            {% endfor %}
            <input type="hidden" name="question_id" value="{{ loop.index0 }}">
            <button type="submit">Next</button>
        </form>
    ''', question=question, loop=enumerate(questions))

@app.route('/results')
def results():
    if 'authenticated' not in session:
        return redirect('/')
    
    score = session.pop('score', 0)
    answers = session.pop('answers', [])
    
    return render_template_string('''
        <h1>Results</h1>
        <p>Your score: {{ score }}</p>
        <h2>Review Answers:</h2>
        <ul>
            {% for question, selected, correct in answers %}
                <li>{{ question }} - Your answer: {{ selected }}; Correct answer: {{ correct }}</li>
            {% endfor %}
        </ul>
        <a href="/">Logout</a>
    ''', score=score, answers=answers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)