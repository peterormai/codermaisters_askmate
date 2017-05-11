from flask import Flask, render_template, request, redirect
import time
import base64

app = Flask(__name__)


@app.route("/new_question")
def question():
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def submit_new_question():
    new_question_title = request.form["new_question"]
    new_question_title_encoded = base64.b64encode(new_question_title.encode())
    new_question_message = request.form["new_question_long"]
    new_question_message_encoded = base64.b64encode(new_question_message.encode())
    picture_url = request.form["picture"]
    count_view = 0
    count_like = 0
    question_time = time.time()
    new_question_title_decoded = base64.b64encode(new_question_title_encoded)
    print(new_question_title_decoded)

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
        file.write(str(new_question_title_encoded) + ",")
        file.write(str(new_question_message_encoded) + ",")
        file.write(str(picture_url + "\n"))

    print(new_question_title_decoded)
    return render_template("new_question.html")

    # redirect to Peti's page at the end with ...question/current_id !!!!!! ****


if __name__ == "__main__":
    app.run()
