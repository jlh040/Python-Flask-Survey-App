from flask import Flask, redirect, request, flash, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = '0c2b6x'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
questions = satisfaction_survey.questions

@app.route('/')
def show_start_page():
    """Display the title and instructions of the survey,
    and a button to start the survey.
    """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)

@app.route('/questions/<int:question_num>')
def handle_question(question_num):
    """Display a form that asks the user a question, shows the choices and
    a submit button.
    """
    correct_page_number = len(responses)
    if question_num != correct_page_number:
        question_num = correct_page_number

    current_question_obj = questions[question_num]
    current_question = current_question_obj.question
    choices = current_question_obj.choices

    return render_template('question-page.html', question_num = question_num,
    current_question = current_question, choices = choices)

@app.route('/answer', methods=['POST'])
def send_answer():
    """Append the answer to the responses list, and then
    redirect the user to the next page.
    """

    answer = request.form['radio-question']
    responses.append(answer)
    page_number = len(responses)
    
    if page_number == len(questions):
        return redirect('/thank_you_page')
    else:
        return redirect(f'/questions/{page_number}')

@app.route('/thank_you_page')
def show_thanks():
    return render_template('thanks.html')
