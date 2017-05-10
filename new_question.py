from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/new_question")
def question():
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def submit_new_question():
    new_question = request.form["new_question"]
    new_question_long = request.form["new_question_long"]

    question_id = 0
    with open("new_questions.csv", "r") as file:
        for i in file:
            if i == "\n":
                question_id = int(question_id) + 1

    with open("new_questions.csv", "a") as file:
        file.write(str(question_id + "\t"))
        file.write(str(new_question + "\t"))
        file.write(str(new_question_long + "\n"))

    return render_template("new_question.html")

if __name__ == "__main__":
    app.run()
