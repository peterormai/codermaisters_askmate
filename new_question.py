from flask import Flask, render_template, request, redirect
import time

app = Flask(__name__)


@app.route("/new_question")
def question():
    return render_template("new_question.html")


def count_lines():
    with open("new_questions.csv") as file:
        for i, line in enumerate(file):
            pass


@app.route("/new_question", methods=["POST"])
def submit_new_question():
    new_question_title = request.form["new_question"]
    new_question_message = request.form["new_question_long"]
    count_view = 0
    count_like = 0
    question_time = time.time()

    with open("new_questions.csv", "r") as file:
        data_list = file.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        if len(data_list) > 0:
            question_id = str(int(data_list[-1][0]) + 1)
        else:
            question_id = 0

    with open("new_questions.csv", "a") as file:
        file.write(str(question_id) + ",")
        file.write(str(question_time) + ",")
        file.write(str(count_view) + ",")
        file.write(str(count_like) + ",")
        file.write(str(new_question_title + ","))
        file.write(str(new_question_message + "\n"))

    return render_template("new_question.html")


if __name__ == "__main__":
    app.run()
