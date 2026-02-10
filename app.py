import os, json, random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'nec-trainer-secret-key-2024'

# Sample NEC 2023 questions
SAMPLE_QUESTIONS = [
    {"question": "What is the maximum overcurrent protection for a 20A circuit?", "options": ["15A", "20A", "25A", "30A"], "correct": 1},
    {"question": "What is the minimum wire size for a 200A service?", "options": ["4 AWG", "2 AWG", "1/0 AWG", "3/0 AWG"], "correct": 2},
    {"question": "What is the maximum distance for a GFCI outlet in a bathroom?", "options": ["3 feet", "4 feet", "6 feet", "8 feet"], "correct": 2},
    {"question": "What does NEC stand for?", "options": ["National Electrical Code", "National Electric Commission", "New Electrical Code", "National Energy Code"], "correct": 0},
    {"question": "What is the standard voltage for residential service in the US?", "options": ["110V", "120/240V", "208V", "277/480V"], "correct": 1},
    {"question": "What is the maximum amperage for a 12 AWG wire at 60°C?", "options": ["15A", "20A", "25A", "30A"], "correct": 1},
    {"question": "What is the minimum burial depth for direct burial cable?", "options": ["6 inches", "12 inches", "18 inches", "24 inches"], "correct": 1},
    {"question": "What type of breaker is used for motor circuits?", "options": ["Standard breaker", "GFCI breaker", "Motor breaker", "Thermal-magnetic breaker"], "correct": 2},
    {"question": "What is the maximum voltage drop allowed for branch circuits?", "options": ["2%", "3%", "5%", "7%"], "correct": 2},
    {"question": "What does GFCI stand for?", "options": ["Ground Fault Circuit Interrupter", "Ground Fault Current Indicator", "Grounded Fault Circuit Interrupter", "Ground Fault Control Interface"], "correct": 0},
]

try:
    with open('questions.json', 'r') as f:
        ALL_QUESTIONS = json.load(f)
except:
    ALL_QUESTIONS = SAMPLE_QUESTIONS

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        pin = request.form.get('pin', '').strip()
        
        if name and len(pin) == 4 and pin.isdigit():
            session['user'] = name
            session['attempts'] = 0
            session['correct'] = 0
            session['history'] = []
            return redirect(url_for('dashboard'))
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>NEC 2023 Trainer - Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .card {
                box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                border: none;
                border-radius: 12px;
            }
            .card-body {
                padding: 40px;
            }
        </style>
    </head>
    <body>
        <div class="container" style="max-width: 400px;">
            <div class="card">
                <div class="card-body">
                    <h2 class="mb-4 text-center">📚 NEC 2023 Trainer</h2>
                    <form method="post">
                        <div class="mb-3">
                            <input type="text" class="form-control form-control-lg" name="name" placeholder="Enter your name" required autofocus>
                        </div>
                        <div class="mb-4">
                            <input type="password" class="form-control form-control-lg" name="pin" maxlength="4" placeholder="Enter PIN (1234)" required>
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100">Login</button>
                    </form>
                    <p class="text-center mt-3 text-muted small">Demo PIN: 1234</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session.get('user', 'User')
    attempts = session.get('attempts', 0)
    correct = session.get('correct', 0)
    accuracy = round((correct / attempts * 100), 1) if attempts > 0 else 0
    
    html = f'''\
    <!DOCTYPE html>\
    <html>\
    <head>\
        <meta charset="UTF-8">\
        <meta name="viewport" content="width=device-width, initial-scale=1">\
        <title>NEC Trainer - Dashboard</title>\
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">\
        <style>\
            body {{\
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\
                min-height: 100vh;\
                padding: 20px 0;\
            }}\
            .card {{\
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);\
                border: none;\
                border-radius: 12px;\
            }}\
            .stat-box {{\
                background: #f8f9fa;\
                padding: 20px;\
                border-radius: 10px;\
                text-align: center;\
                border-left: 4px solid #667eea;\
            }}\
            .stat-box h4 {{\
                color: #667eea;\
                font-weight: 700;\
                margin: 10px 0 0 0;\
            }}\
        </style>\
    </head>\
    <body>\
        <div class="container py-4" style="max-width: 900px;">\
            <div class="card">\
                <div class="card-body">\
                    <div class="d-flex justify-content-between align-items-center mb-4">\
                        <h2 class="mb-0">Welcome, {user}! 👋</h2>\
                        <a href="/logout" class="btn btn-outline-danger btn-sm">Logout</a>\
                    </div>\
                    \ 
                    <div class="row mb-4">\
                        <div class="col-6 col-md-3 mb-3">\
                            <div class="stat-box">\
                                <div class="text-muted small">Questions Answered</div>\
                                <h4>{attempts}</h4>\
                            </div>\
                        </div>\
                        <div class="col-6 col-md-3 mb-3">\
                            <div class="stat-box">\
                                <div class="text-muted small">Correct Answers</div>\
                                <h4>{correct}</h4>\
                            </div>\
                        </div>\
                        <div class="col-6 col-md-3 mb-3">\
                            <div class="stat-box">\
                                <div class="text-muted small">Accuracy Rate</div>\
                                <h4>{accuracy}%</h4>\
                            </div>\
                        </div>\
                        <div class="col-6 col-md-3 mb-3">\
                            <div class="stat-box">\
                                <div class="text-muted small">Available Questions</div>\
                                <h4>{len(ALL_QUESTIONS)}</h4>\
                            </div>\
                        </div>\
                    </div>\
                    \ 
                    <hr>\
                    <h5 class="mb-3">📋 Select a Quiz</h5>\
                    <div class="d-grid gap-2">\
                        <a href="/quiz/10" class="btn btn-primary btn-lg">10 Questions Quiz</a>\
                        <a href="/quiz/20" class="btn btn-primary btn-lg">20 Questions Quiz</a>\
                        <a href="/quiz/50" class="btn btn-primary btn-lg">50 Questions Quiz</a>\
                        <a href="/quiz/100" class="btn btn-primary btn-lg">100 Questions Quiz</a>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </body>\
    </html>\
    '''
    return render_template_string(html)

@app.route('/quiz/<int:num>')
def quiz(num):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    num = min(num, len(ALL_QUESTIONS))
    selected = random.sample(ALL_QUESTIONS, num)
    session['quiz_questions'] = selected
    session['quiz_index'] = 0
    session['quiz_score'] = 0
    
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if 'quiz_questions' not in session:
        return redirect(url_for('dashboard'))
    
    questions = session['quiz_questions']
    index = session.get('quiz_index', 0)
    
    if request.method == 'POST':
        answer = request.form.get('answer', '')
        current_q = questions[index]
        
        if str(answer).isdigit():
            answer = int(answer)
            if answer == current_q['correct']:
                session['quiz_score'] = session.get('quiz_score', 0) + 1
                session['correct'] = session.get('correct', 0) + 1
        
        session['attempts'] = session.get('attempts', 0) + 1
        session['quiz_index'] = index + 1
        
        if session['quiz_index'] >= len(questions):
            return redirect(url_for('results'))
        
        return redirect(url_for('question'))
    
    if index >= len(questions):
        return redirect(url_for('results'))
    
    current_question = questions[index]
    progress = round((index / len(questions)) * 100, 1)
    
    options_html = ''.join([
        f'<div class="form-check mb-2">'\
        f'<input class="form-check-input" type="radio" name="answer" id="option{i}" value="{i}" required>'\
        f'<label class="form-check-label" for="option{i}">{opt}</label>'\
        f'</div>'\
        for i, opt in enumerate(current_question['options'])
    ])
    
    html = f'''\
    <!DOCTYPE html>\
    <html>\
    <head>\
        <meta charset="UTF-8">\
        <meta name="viewport" content="width=device-width, initial-scale=1">\
        <title>NEC Trainer - Question</title>\
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">\
        <style>\
            body {{\
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\
                min-height: 100vh;\
                padding: 20px 0;\
            }}\
            .card {{\
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);\
                border: none;\
                border-radius: 12px;\
            }}\
            .progress {{\
                height: 25px;\
            }}\
        </style>\
    </head>\
    <body>\
        <div class="container py-4" style="max-width: 800px;">\
            <div class="card">\
                <div class="card-body">\
                    <div class="d-flex justify-content-between align-items-center mb-3">\
                        <h5 class="mb-0">Question {index + 1} of {len(questions)}</h5>\
                        <a href="/dashboard" class="btn btn-sm btn-outline-secondary">Exit</a>\
                    </div>\
                    \ 
                    <div class="mb-4">\
                        <div class="progress">\
                            <div class="progress-bar" style="width: {progress}%"></div>\
                        </div>\
                    </div>\
                    \ 
                    <h4 class="mb-4">{current_question['question']}</h4>\
                    \ 
                    <form method="post">\
                        {options_html}\
                        <div class="mt-4">\
                            <button type="submit" class="btn btn-primary btn-lg">Next Question</button>\
                        </div>\
                    </form>\
                </div>\
            </div>\
        </div>\
    </body>\
    </html>\
    '''
    return render_template_string(html)

@app.route('/results')
def results():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    score = session.get('quiz_score', 0)
    total = len(session.get('quiz_questions', []))
    percentage = round((score / total * 100), 1) if total > 0 else 0
    
    if percentage >= 80:
        message = "🎉 Excellent! You passed!"
        color = "success"
    elif percentage >= 60:
        message = "✅ Good job! Keep practicing!"
        color = "info"
    else:
        message = "📚 Keep studying and try again!"
        color = "warning"
    
    html = f'''\
    <!DOCTYPE html>\
    <html>\
    <head>\
        <meta charset="UTF-8">\
        <meta name="viewport" content="width=device-width, initial-scale=1">\
        <title>NEC Trainer - Results</title>\
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">\
        <style>\
            body {{\
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\
                min-height: 100vh;\
                padding: 20px 0;\
                display: flex;\
                align-items: center;\
                justify-content: center;\
            }}\
            .card {{\
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);\
                border: none;\
                border-radius: 12px;\
            }}\
            .score-circle {{\
                width: 150px;\
                height: 150px;\
                border-radius: 50%;\
                display: flex;\
                align-items: center;\
                justify-content: center;\
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\
                color: white;\
                font-size: 48px;\
                font-weight: 700;\
                margin: 0 auto 20px;\
            }}\
        </style>\
    </head>\
    <body>\
        <div class="container" style="max-width: 600px;">\
            <div class="card">\
                <div class="card-body text-center py-5">\
                    <h2 class="mb-4">Quiz Complete! 🏁</h2>\
                    <div class="score-circle">{percentage}%</div>\
                    <h4 class="text-{color} mb-4">{message}</h4>\
                    <p class="h5 mb-4">You scored <strong>{score} out of {total}</strong> questions correctly.</p>\
                    <div class="d-grid gap-2">\
                        <a href="/dashboard" class="btn btn-primary btn-lg">Back to Dashboard</a>\
                        <a href="/logout" class="btn btn-outline-secondary">Logout</a>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </body>\
    </html>\
    '''
    return render_template_string(html)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)