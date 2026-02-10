from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    progress = db.Column(db.PickleType, default={})  # Track user progress

# Quiz questions
questions = [
    {'question': 'What is 2 + 2?', 'options': ['3', '4', '5'], 'answer': '4'},
    {'question': 'What is the capital of France?', 'options': ['Berlin', 'Madrid', 'Paris'], 'answer': 'Paris'},
]

@app.route('/')
def home():
    return render_template_string('''
    <h1>Welcome to the NEC 2023 Trainer</h1>
    <a href="/login">Login</a>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials!'
    return render_template_string('''
    <h1>Login</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    ''')

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))
    return render_template_string('''
    <h1>Dashboard</h1>
    <p>Welcome, {{ username }}!</p>
    <a href="/quiz">Start Quiz</a><br>
    ''', username=user.username)

@app.route('/quiz')
def quiz():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))
    return render_template_string('''
    <h1>Quiz</h1>
    <form method="POST" action="/submit_quiz">
        {% for question in questions %}
            <p>{{ question.question }}</p>
            {% for option in question.options %}
                <input type="radio" name="q{{ loop.index }}" value="{{ option }}">{{ option }}<br>
            {% endfor %}
        {% endfor %}
        <input type="submit" value="Submit">
    </form>
    ''')

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))
    score = 0
    for i, question in enumerate(questions):
        user_answer = request.form.get(f'q{i + 1}')
        if user_answer == question['answer']:
            score += 1
    user.progress[datetime.now().strftime('%Y-%m-%d')] = score
    db.session.commit()
    return f'Your score: {score}/{len(questions)}\nProgress updated!'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)