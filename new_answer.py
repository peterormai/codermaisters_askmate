from flask import Flask, render_template, request, redirect
import time
# Nézd át az importot
app = Flask(__name__)


@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    with open('question.csv') as file:
        question_list = [question.split(',') for question in file.read().splitlines()]
    selected_question = ''
    for question in question_list:
        if int(question[0]) == int(question_id):
            selected_question = question
            break
    webpage_title = 'Post an Answer'
    return render_template('/new_answer.html',
                           webpage_title=webpage_title,
                           question=selected_question)


@app.route('/question/<int:question_id>/new_answer', methods=['POST'])
def add_answer(question_id):
    with open('answer.csv') as file:
        answer_id = int([item.split(',') for item in file.read().splitlines()][-1][0]) + 1 #Ne így legyen
    message = request.form['answer']
    image = ''
    with open('answer.csv', 'a') as file:
        file.write(str(answer_id) + ',')
        file.write(str(time.time()) + ',')
        file.write(str(0) + ',')    # Vote number
        file.write(str(question_id) + ',')
        file.write(str(message) + ',')  # Át akarom írni!!
        file.write(str(image) + '\n')
    return redirect('/')


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
