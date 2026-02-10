from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Inline HTML templates
login_template = '''<!doctype html>\n<html><body>\n<h2>Login</h2>\n<form method='POST'>\nUsername: <input name='username'>\n<input type='submit' value='Login'>\n</form>\n</body></html>'''

dashboard_template = '''<!doctype html>\n<html><body>\n<h2>Dashboard</h2>\n<p>Welcome, {{ username }}!</p>\n<a href='{{ url_for("quiz") }}'>Take the Quiz</a>\n<a href='{{ url_for("logout") }}'>Logout</a>\n</body></html>'''

quiz_template = '''<!doctype html>\n<html><body>\n<h2>Quiz</h2>\n<form method='POST'>\n{{ question }}\n<br>\n<input type='radio' name='answer' value='1'>{{ option1 }}<br>\n<input type='radio' name='answer' value='2'>{{ option2 }}<br>\n<input type='submit' value='Submit'>\n</form>\n<p>Your score: {{ score }}</p>\n</body></html>'''

# Mock Questions for Quiz
questions = [
    {"question": "What is 2 + 2?", "option1": "3", "option2": "4", "answer": 2},
    {"question": "What is 3 + 5?", "option1": "9", "option2": "8", "answer": 2}
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('dashboard'))
    return render_template_string(login_template)

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template_string(dashboard_template, username=username)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected_answer = int(request.form['answer'])
        question_index = session.get('question_index', 0)
        is_correct = selected_answer == questions[question_index]['answer']
        score = session.get('score', 0) + (1 if is_correct else 0)
        session['score'] = score
        question_index += 1
        session['question_index'] = question_index
        if question_index < len(questions):
            return render_template_string(quiz_template,
                question=questions[question_index]['question'],
                option1=questions[question_index]['option1'],
                option2=questions[question_index]['option2'],
                score=score)
        else:
            return f'Quiz finished! Your score: {score}'
    else:
        session['score'] = 0
        session['question_index'] = 0
        return render_template_string(quiz_template,
            question=questions[0]['question'],
            option1=questions[0]['option1'],
            option2=questions[0]['option2'],
            score=0)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)