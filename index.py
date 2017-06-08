from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import queries
from datetime import datetime
import smtplib
from flask import Response, abort, session, flash
from functools import wraps

app = Flask(__name__)


# #######################USER AUTHENTICATION########################
app.config.update(
    SECRET_KEY='123124124512312'
)


def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if session.get("role") == 'user':
            return function(*args, **kwargs)
        else:
            flash('You need to login')
            return redirect(url_for('login'))
    return wrap


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_check = queries.check_user(username, password)
        if user_check is not None:
            session['username'] = username
            session['role'] = user_check[0]
            return redirect(url_for('show_latest_five_questions'))
        else:
            return abort(401)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('show_latest_five_questions'))


@app.route('/password_recovery')
def show_password_recovery():
    return render_template('password_recovery.html')


@app.route('/password_recovery', methods=['POST'])
def do_password_recovery():
    email = request.form['email']
    new_password = queries.password_recovery(email)
    msg = 'You requested a new password for your account at Codermeisters.com \n Your new password is: {0}'.format(
        new_password).encode('utf-8').strip()
    send_mail('barnabastoth94@gmail.com', 'fanatic99', email, msg)
    return redirect(url_for('show_latest_five_questions'))


def send_mail(sender_email, sender_password, target_email, message):
    import smtplib

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    msg = message
    server.sendmail(sender_email, target_email, msg)
    server.quit()
    # #######################USER AUTHENTICATION########################
    # #######################EXTRA FUNCTIONS########################


def redirect_url(default='index'):
    """
    It redirects to the previous page.
    """
    return request.args.get('next') or \
        request.referrer or \
        url_for(default)


@app.errorhandler(404)
def page_not_found(e):
    """
    Error handling for wrong DNS address request.
    """
    return render_template('404.html')

# #######################EXTRA FUNCTIONS########################


# #######################QUESTIONS########################
@app.route('/')
def show_latest_five_questions():
    """
    Show the latest 5 submitted questions.
    """
    title = "Super Sprinter 3000"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    data_list = queries.get_latest_five_questions()
    return render_template('index.html', data_list=data_list, title=title, top_menu=top_menu)


@app.route('/list')
@login_required
def list_questions():
    """
    Lists all questions from the database.
    """
    data_list = queries.get_all_questions()
    title = "Cödermeisters's ask-mate"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    return render_template('index.html', title=title, data_list=data_list, top_menu=top_menu)


@app.route("/like/<int:id>/<int:like_value>")
def question_handle_like(id, like_value):
    """Change the number of likes according to user.
    Receives three arguments:
        - id: ID row
        - like_value: number of current likes (default is set to ‘0’)
    Overwrites old data with new data and redirects to the page where the like button is placed.
    """
    if like_value == 1:
        queries.handle_question_like(id, like_value)
    else:
        queries.handle_question_like(id, -1)
    return redirect(redirect_url())


@app.route("/question/<int:id>/edit")
def show_question(id):
    """
    Shows the question edit page with the chosen question's informations.
    """
    creator_username = queries.creator_username('question', id)
    if creator_username == session.get("username") or session.get("role") == 'admin':
        selected_question = queries.show_one_question(id)[0]
        return render_template('update.html', selected_question=selected_question, id=id, username='peter')
    else:
        return redirect('/')


@app.route("/question/<int:id>/edit", methods=["POST"])
def update_question(id):
    """
    Saves the modified question information to the database.
    """
    selected_question = request.form["question_update"]
    selected_message = request.form["message_update"]
    queries.update_question_query(selected_question, selected_message, id)
    return redirect(url_for('show_latest_five_questions'))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_one_question(question_id):
    """
    The selected question will be removed with all the associated answers and comments from the database permanently.
    """
    creator_username = queries.creator_username('question', question_id)
    if creator_username == session.get("username") or session.get("role") == 'admin':
        queries.delete_question(question_id)
        return redirect(url_for('show_latest_five_questions'))
    else:
        flash("You are not allowed to use this function!")
        return redirect(redirect_url())


@app.route("/new_question")
@login_required
def show_new_question():
    """
    Show the new_question page.
    """
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def new_question():
    """
    It saves the question and all of entered details to the database.
    """
    submission_time = str(datetime.now())[:-7]
    view_number = 0
    vote_number = 0
    title = request.form["new_question"]
    creator_username = session.get('username')
    user_id = queries.creator_id(creator_username)
    if len(title) < 10:
        return redirect(url_for('new_question'))
    else:
        message = request.form["new_question_long"]
        image = request.form['picture']
        queries.submit_new_question(submission_time, view_number, vote_number, title, message, image, user_id)
        return redirect(url_for('show_latest_five_questions'))
# #######################QUESTIONS########################


# #######################ANSWERS########################
@app.route('/question/<int:question_id>')
def question_display(question_id):
    """
    The related question will be displayed with answers and comments.
    """
    webpage_title = 'Question & answers'
    selected_question = queries.get_question_details(question_id)[0]
    related_answers = queries.get_question_answers(question_id)
    question_comment = queries.get_question_comments(question_id)

    answer_ids = queries.get_answer_comment_ids(question_id)
    answer_id_numbers = []
    for item in answer_ids:
        answer_id_numbers.append("".join(map(str, item)))

    answer_comment = []
    for answer_id in answer_id_numbers:
        answer_comment.append(queries.get_answer_comments(int(answer_id)))
    return render_template('question_display.html',
                           question=selected_question,
                           answers=related_answers,
                           webpage_title=webpage_title,
                           question_comment=question_comment,
                           answer_comment=answer_comment,
                           answer_ids=answer_id_numbers)


@app.route("/like/<int:answer_id>/<from_page>/<int:like_value>")
def answer_handle_like(answer_id, from_page, like_value):
    """Change the number of votes according to user.
    Receives two arguments:
        - answer_id
        - like_value: number of current likes (default is set to ‘0’)
    Overwrites old data with new data and redirects to the current page.
    """
    if like_value == 1:
        queries.handle_answer_like(answer_id, like_value)
    else:
        queries.handle_answer_like(answer_id, -1)
    return redirect(redirect_url())


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    """
    The selected answer will be removed from the database permanently.
    """
    creator_username = queries.creator_username('answer', answer_id)
    if creator_username == session.get("username") or session.get("role") == 'admin':
        queries.delete_one_answer(answer_id)
    return redirect(redirect_url())


@app.route('/question/<int:question_id>/new_answer')
@login_required
def new_answer(question_id):
    """
    It diplays a page with the selected question details. With a field where the user can write a new answer to it.
    """
    webpage_title = 'Post an Answer'
    question = queries.get_question_details(question_id)[0]
    return render_template('/new_answer.html', webpage_title=webpage_title, question=question)


@app.route('/question/<int:question_id>/new_answer', methods=['POST'])
def add_answer(question_id):
    """
    Saves the new answer by the user input to a specific question.
    """
    if len(request.form['answer']) < 10:
        return redirect('/question/' + str(question_id) + '/new_answer')
    else:
        submission_time = str(datetime.now())[:-7]
        vote_number = 0
        message = request.form['answer']
        image = request.form['picture']
        creator_username = session.get('username')
        user_id = queries.creator_id(creator_username)
        queries.add_new_answer(submission_time, vote_number, question_id, message, image, user_id)
        return redirect('/question/' + str(question_id))
# #######################ANSWERS########################


# #######################COMMENTS########################
@app.route('/question/<int:question_id>/new_comment')
@login_required
def new_comment(question_id):
    """
    It diplays a page with a field where the user can write a new comment to the selected question.
    One argument: specific question ID of the question.
    """
    action_variable = 'question'
    webpage_title = 'Post a comment'
    details = queries.get_question_details(question_id)[0]
    return render_template('/new_comment.html', webpage_title=webpage_title, details=details, action_variable=action_variable, question_id=question_id)


@app.route('/question/<int:question_id>/new_comment', methods=['POST'])
def add_new_comment(question_id):
    """
    Saves the given comment by the user to a specific question.
    """
    submission_time = str(datetime.now())[:-7]
    message = request.form['answer']
    creator_username = session.get('username')
    user_id = queries.creator_id(creator_username)
    queries.submit_new_question_comment(question_id, message, submission_time, user_id)
    return redirect('/question/' + str(question_id))


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    """
    Delete a comment from a question or an answer.
    """
    creator_username = queries.creator_username('comment', comment_id)
    if creator_username == session.get("username") or session.get("role") == 'admin':
        queries.delete_comment(comment_id)
    return redirect(redirect_url())


@app.route('/answer/<int:answer_id>/new_comment')
@login_required
def new_answer_comment(answer_id):
    """
    It diplays a page with a field where the user can write a new comment to the selected answer.
    One argument: specific question ID of the question.
    """
    action_variable = 'answer'
    webpage_title = 'Post a comment'
    details = queries.show_one_answer(answer_id)[0]
    question_id = queries.search_question_id(answer_id)[0][0]
    return render_template('/new_comment.html', webpage_title=webpage_title,
                           details=details, action_variable=action_variable, question_id=question_id)


@app.route('/answer/<int:answer_id>/new_comment', methods=['POST'])
def add_new_answer_comment(answer_id):
    """
    Saves the given comment by the user to a specific answer.
    """
    submission_time = str(datetime.now())[:-7]
    message = request.form['answer']
    creator_username = session.get('username')
    user_id = queries.creator_id(creator_username)
    queries.submit_new_answer_comment(answer_id, message, submission_time, user_id)
    question_id = queries.search_question_id(answer_id)[0][0]
    return redirect('/question/' + str(question_id))
# #######################COMMENTS########################


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
