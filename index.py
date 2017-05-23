from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import time
import base64
import queries

# EZEKET MÓDOSÍTANI
import kristof
import helga
import barna
import peti


app = Flask(__name__)

# Main page


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def questions_list():
    result = kristof.list_questions()
    return result


@app.route("/sortby", methods=['POST'])
def sorting():
    result = helga.sort_by()
    return result


@app.route("/like/<int:id>/<int:like_value>/<from_page>", methods=['GET'])
def like():
    result = kristof.handle_like()
    return result


@app.route("/like/<int:answer_id>/<from_page>/<int:like_value>", methods=['GET'])
def ans_like():
    result = kristof.answer_handle_like()
    return result


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
def ques_display():
    result = peti.question_display()
    return result


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
def del_ans():
    result = peti.delete_answer()
    return result


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def del_ques():
    result = kristof.delete_question()
    return result


# New answer
@app.route('/question/<int:question_id>/new_answer')
def new_ans():
    result = helga.new_answer()
    return result


@app.route('/question/<int:question_id>/new_answer', methods=['POST'])
def add_ans():
    result = helga.add_answer()
    return result


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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
