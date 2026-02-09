from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/exam', methods=['POST'])
def exam():
    data = request.get_json()
    # Process the exam data
    return jsonify({'message': 'Exam processed successfully!', 'data': data})

if __name__ == '__main__':
    app.run(debug=True)