from ast import Param
from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)

url = "https://questionic-server.onrender.com/get-questions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-test', methods=['POST'])
def generate_test():
    try:
        # Fetch questions with subject_id parameter
        params = {'subject_id': '1'}
        params = json.dumps(params)
        response = requests.get(url, params=params)
        questions = response.json()
        
        # Print questions to console for debugging
        print("Fetched questions:", questions)
        
        return render_template('test.html', questions=questions)
    
    except Exception as e:
        return str(e)

@app.route('/submit-test', methods=['POST'])
def submit_test():
    questions = request.form.getlist('questions')
    selected_answers = request.form.getlist('answers')
    questions = eval(questions[0])  # Convert string representation back to list
    
    score = 0
    corrections = []

    for i, question in enumerate(questions):
        correct_answer = question['correct_answer']
        selected_answer = int(selected_answers[i])
        is_correct = correct_answer == selected_answer
        if is_correct:
            score += 1
        corrections.append({
            'question': question,
            'selected_answer': selected_answer,
            'is_correct': is_correct
        })
    
    return render_template('result.html', score=score, corrections=corrections)

if __name__ == '__main__':
    app.run(debug=True)
