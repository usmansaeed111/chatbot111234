from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

questions = [
    "Have you been feeling unusually irritable or easily angered lately?",
    "Do you frequently experience outbursts of anger or have difficulty controlling your anger?",
    "Are you frequently experiencing a sense of being overwhelmed or unable to cope with daily tasks or responsibilities?",
    "Do you often find it challenging to relax or find time for yourself?",
    "Do you frequently feel restless, on edge, or have difficulty sitting still?",
    "Do you often experience racing thoughts, excessive worry, or have trouble controlling your worry?",
    "Have you noticed a persistent lack of interest or pleasure in activities that you used to enjoy?",
    "Do you often feel sad, down, or hopeless, with little interest in the future?",
    "Do you frequently experience physical symptoms such as tension, headaches, or digestive issues when you're under pressure?",
    "Are you finding it challenging to manage your anger or stress in a healthy way?"
]

answers = [None] * len(questions)  # Initialize answers list

current_question_index = 0  # Track the current question being asked

assessment_in_progress = False  # Flag to track if assessment is in progress

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global current_question_index, assessment_in_progress

    user_input = request.form['user_input']

    if assessment_in_progress:
        return handle_assessment(user_input)
    else:
        return handle_normal_conversation(user_input)

def handle_normal_conversation(user_input):
    global assessment_in_progress

    if "start" in user_input.lower():
        assessment_in_progress = True
        current_question_index = 0
        return jsonify({'response': questions[current_question_index]})
    else:
        return jsonify({'response': "Type 'start' to begin the assessment. Give answer in the form of 'yes' or 'no'."})

# ... (previous code)

def handle_assessment(user_input):
    global current_question_index

    if current_question_index < len(questions):
        answers[current_question_index] = user_input
        current_question_index += 1

        if current_question_index < len(questions):
            return jsonify({'response': questions[current_question_index]})
        else:
            result = calculate_mental_health_score(answers)
            reset_assessment()
            return jsonify({'response': "Thank you for participating. Here is the assessment result:\n" + result})
    else:
        reset_assessment()
        return jsonify({'response': "I'm sorry, I didn't understand that."})

def calculate_mental_health_score(answers):
    disorders = {
        "Anxiety": [4, 5],
        "Depression": [6, 7],
        "Stress": [2, 3, 8, 9],
        "Anger": [0, 1, 8, 9]
    }

    disorder_percentages = {disorder: 0 for disorder in disorders}

    for i, answer in enumerate(answers):
        for disorder, indices in disorders.items():
            if i in indices and answer == "yes":
                disorder_percentages[disorder] += 1

    total_questions = len(answers)
    overall_percentage = 100

    disorder_percentage_sum = sum(disorder_percentages.values())
    disorder_percentage_scale = overall_percentage / disorder_percentage_sum

    disorder_percentages = {disorder: percentage * disorder_percentage_scale for disorder, percentage in disorder_percentages.items()}

    interpretation = "Based on the responses, you may be experiencing the following mental health disorders:"
    for disorder, percentage in disorder_percentages.items():
        interpretation += "\n- {} ({}%)".format(disorder, round(percentage, 2))

    return interpretation

def reset_assessment():
    global current_question_index, assessment_in_progress
    current_question_index = 0
    assessment_in_progress = False

if __name__ == '__main__':
    app.run(debug=True)

