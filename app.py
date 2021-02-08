from flask import Flask, redirect, request, flash, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = '0c2b6x'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

questions = satisfaction_survey.questions

@app.route('/')
def show_start_page():
    """Display the title and instructions of the survey,
    and a button to start the survey.
    """
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title = title, instructions = instructions)

@app.route('/set-session', methods=["POST"])
def set_session():
    """Store an empty list in the session and send it as a cookie to the user"""
    session['responses'] = []
    return redirect('/questions/0')


@app.route('/questions/<int:question_num>')
def handle_question(question_num):
    """Display a form that asks the user a question, and also shows the 
    user their choices and a submit button.
    """
    correct_page_number = len(session['responses'])
    
    if len(session['responses']) == len(questions):
        return redirect('/thank_you_page')
    elif question_num != correct_page_number:
        question_num = correct_page_number
        flash('Answer the correct question please!', 'error')
    
    current_question_obj = questions[question_num]
    current_question = current_question_obj.question
    choices = current_question_obj.choices

    return render_template('question-page.html', question_num = question_num,
    current_question = current_question, choices = choices)

@app.route('/answer', methods=['POST'])
def send_answer():
    """Append the answer to the session, and then
    redirect the user to the next page.
    """
    answer = request.form['radio-question']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    page_number = len(session['responses'])
    
    if page_number == len(questions):
        return redirect('/thank_you_page')
    else:
        return redirect(f'/questions/{page_number}')

@app.route('/thank_you_page')
def show_thanks():
    """Show the user a thank you page"""
    
    return render_template('thanks.html')
