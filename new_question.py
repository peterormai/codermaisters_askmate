from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/new_question")
def new_question():
    return render_template("new_question.html")

if __name__ == "__main__":
    app.run()