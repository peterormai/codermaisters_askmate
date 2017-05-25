from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import queries
from datetime import datetime


app = Flask(__name__)

# #######################EXTRA FUNCTIONS########################


def redirect_url(default='index'):
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
        - from_page: name of the current page
    Overwrites old data with new data and redirects to the current page.
    """
    if like_value == 1:
        queries.handle_question_like(id, like_value)
    else:
        queries.handle_question_like(id, -1)
    return redirect(redirect_url())


@app.route("/question/<int:id>/edit")
def show_question(id):
    selected_question = queries.show_one_question(id)[0]
    return render_template('update.html', selected_question=selected_question, id=id)


@app.route("/question/<int:id>/edit", methods=["POST"])
def update_question(id):
    selected_question = request.form["question_update"]
    selected_message = request.form["message_update"]
    queries.update_question_query(selected_question, selected_message, id)
    return redirect("/list")


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_one_question(question_id):
    """
    Given the right argument, the related question will be removed with all the answers from the database permanently. 
    """
    queries.delete_question(question_id)
    return redirect('/')


@app.route("/new_question")
def show_new_question():
    """
    Show new_question page.
    """
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def new_question():
    """Takes a new question and description from user and encrypts it.
    Receives data fromm the user input, uses BASE64 encryption for title and description.
    Set by default an ID number, creation time, view and like number and save it as a .csv file.
    """
    submission_time = datetime.now()
    view_number = 0
    vote_number = 0
    title = request.form["new_question"]
    if len(title) < 10:
        return redirect('new_question')
    else:
        message = request.form["new_question_long"]
        image = request.form['picture']
        queries.submit_new_question(submission_time, view_number, vote_number, title, message, image)
        return redirect('/list')
# #######################QUESTIONS########################


# #######################ANSWERS########################
@app.route('/question/<int:question_id>')
def question_display(question_id):
    """
    Display the question with all the answers below.
    Given the right argument, the related question will be displayed with answers to it.
    """
    webpage_title = 'Question & answers'
    selected_question = queries.get_question_details(question_id)[0]
    related_answers = queries.get_question_answers(question_id)
    question_comment = queries.get_question_comments(question_id)
    answer_ids = queries.get_answer_comment_ids(question_id)
    answer_comment = []
    for answer_id in answer_ids:
        answer_comment.append(queries.get_answer_comments(int(answer_id)))
    return render_template('question_display.html',
                           question=selected_question,
                           answers=related_answers,
                           webpage_title=webpage_title,
                           question_comment=question_comment,
                           answer_comment=answer_comment,
                           answer_ids=answer_ids)


@app.route("/like/<int:answer_id>/<from_page>/<int:like_value>")
def answer_handle_like(answer_id, from_page, like_value):
    """Change the number of likes according to user.
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
    Given the right argument, the related answer will be removed from the database permanently. 
    """
    queries.delete_one_answer(answer_id)
    return redirect(redirect_url())


@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    """
    The user is able to answer any question.
    One argument: specific question ID of the question.
    """
    webpage_title = 'Post an Answer'
    question = queries.get_question_details(question_id)[0]
    return render_template('/new_answer.html', webpage_title=webpage_title, question=question)


@app.route('/question/<int:question_id>/new_answer', methods=['POST'])
def add_answer(question_id):
    """
    Create a new answer by the user input to a specific question.
    """
    if len(request.form['answer']) < 10:
        return redirect('/question/' + str(question_id) + '/new_answer')
    else:
        submission_time = datetime.now()
        vote_number = 0
        message = request.form['answer']
        image = request.form['picture']
        queries.add_new_answer(submission_time, vote_number, question_id, message, image)
        return redirect('/question/' + str(question_id))
# #######################ANSWERS########################


# #######################COMMENTS########################
@app.route('/question/<int:question_id>/new_comment')
def new_comment(question_id):
    """
    The user is able to comment any question.
    One argument: specific question ID of the question.
    """
    webpage_title = 'Post a comment'
    question = queries.get_question_details(question_id)[0]
    return render_template('/new_comment.html', webpage_title=webpage_title, question=question)


@app.route('/question/<int:question_id>/new_comment', methods=['POST'])
def add_new_comment(question_id):
    submission_time = datetime.now()
    message = request.form['answer']
    queries.submit_new_question_comment(question_id, message, submission_time)
    return redirect('/question/' + str(question_id))


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    """
    Delete a comment from a question or an answer.
    """
    queries.modify_database("""DELETE FROM comment WHERE id={};""".format(comment_id))
    return redirect(redirect_url())
# #######################COMMENTS########################


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
