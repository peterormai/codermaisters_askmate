from flask import Flask, render_template, request, redirect
app = Flask(__name__)


@app.route('/new_answer')
def new_answer():
    return render_template('/new_answer.html')


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
