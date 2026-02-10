from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

# Sample data for users and quizzes
users = {'user1': '1234', 'Jose2381': '5678'}  # PIN login example
quizzes = {10: 'quiz_10', 20: 'quiz_20', 50: 'quiz_50', 100: 'quiz_100'}

# Function to calculate score and explanations
def calculate_score(answers, user_answers):
    score = sum(1 for a, b in zip(answers, user_answers) if a == b)
    return score

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form['pin']
        username = request.form['username']
        
        if username in users and users[username] == pin:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], quizzes=quizzes)
    return redirect(url_for('login'))

@app.route('/quiz/<int:num_questions>', methods=['GET', 'POST'])
def quiz(num_questions):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    questions = random.sample(range(1, 101), num_questions)
    if request.method == 'POST':
        user_answers = request.form.getlist('answers')
        score = calculate_score([1]*num_questions, user_answers)  # Placeholder answers
        return render_template('results.html', score=score, total=num_questions)
    return render_template('quiz.html', questions=questions, num_questions=num_questions)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)