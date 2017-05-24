from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import time
import base64
import queries

import kristof
import helga
import barna
import peti
from datetime import datetime


app = Flask(__name__)

# Main page


def redirect_url(default='index'):
    return request.args.get('next') or \
        request.referrer or \
        url_for(default)


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def questions_list():
    result = kristof.list_questions()
    return result


@app.route("/sortby", methods=['POST'])
def sorting():
    result = helga.sort_by()
    return result


@app.route("/like/<int:id>/<int:like_value>", methods=['GET'])
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


@app.route("/like/<int:answer_id>/<from_page>/<int:like_value>", methods=['GET'])
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


@app.route("/question/<int:id>/edit", methods=["GET"])
def show_ques(id):
    selected_question = queries.show_question(id)[0][0]
    return render_template('update.html', selected_question=selected_question, id=id)


@app.route("/question/<int:id>/edit", methods=["POST"])
def update_quest(id):
    selected_question = request.form["question_update"]
    queries.update_question(selected_question, id)
    return redirect("/list")


@app.errorhandler(404)
def page_not_found(e):
    """
    Error handling for wrong DNS address request.
    """
    return render_template('404.html')


# Display question


@app.route('/question/<int:question_id>')
def question_display(question_id):
    """
    Display the question with all the answers below.
    Given the right argument, the related question will be displayed with answers to it.
    """
    webpage_title = 'Question & answers'
    selected_question = queries.display_question(question_id)[0]
    # item[2] = str(int(item[2]) + 1)   # view counter!!!!!!!!!!!!!!!!!!!!!!!!!!!
    related_answers = queries.display_answer(question_id)
    question_comment = queries.display_question_comment(question_id)
    answer_ids = queries.answer_comment_ids(question_id)
    answer_comment = []
    for answer_id in answer_ids:
        answer_comment.append(queries.display_answer_comment(int(answer_id)))
    return render_template('question_display.html',
                           question=selected_question,
                           answers=related_answers,
                           webpage_title=webpage_title,
                           question_comment=question_comment,
                           answer_comment=answer_comment,
                           answer_ids=answer_ids)


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    """
    Given the right argument, the related answer will be removed from the database permanently. 
    """
    # queries.delete_answer_comment(answer_id)

    # ne a fő oldalre irányítson hanem a kérdés oldalra!!!
    queries.delete_one_answer(answer_id)
    return redirect('/')


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_one_question(question_id):
    """
    Given the right argument, the related question will be removed with all the answers from the database permanently. 
    """
    # queries.delete_answer_comment(answer_id)

    # queries.delete_all_answer(question_id)
    # queries.delete_question_comment(question_id)

    queries.delete_question(question_id)
    return redirect('/')


# New answer
@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    """
    The user is able to answer any question.
    One argument: specific question ID of the question.
    """
    webpage_title = 'Post an Answer'
    question = queries.display_question(question_id)[0]
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
        queries.add_new_anser(submission_time, vote_number, question_id, message, image)
        # jó ez a sok paraméter így?
        return redirect('/question/' + str(question_id))


# New question


@app.route("/new_question")
def question():
    """
    Show new_question page.
    """
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def submit_n_ques():
    result = peti.submit_new_question()
    return result


def show_latest_five_questions():
    """
    Show the latest 5 submitted questions.
    """
    title = "Super Sprinter 3000"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    data_list = queries.fetch_database("""SELECT * FROM question ORDER BY id DESC LIMIT 5;""")
    return render_template('index.html', data_list=data_list, title=title, top_menu=top_menu)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
