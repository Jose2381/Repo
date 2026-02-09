from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!doctype html>
    <title>Flask NEC 2023 Trainer</title>
    <h1>Welcome to Flask NEC 2023 Trainer</h1>
    <p>Learning Flask with inline templates!</p>
    ''')

if __name__ == '__main__':
    app.run(debug=True)