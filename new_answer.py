from flask import Flask, render_template, request, redirect
import time
import file_handler
app = Flask(__name__)


@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    question_list = file_handler.decode_file('question.csv')
    selected_question = ''
    for question in question_list:
        if int(question[0]) == question_id:
            selected_question = question
            break
    webpage_title = 'Post an Answer'
    return render_template('/new_answer.html',
                           webpage_title=webpage_title,
                           question=selected_question)


@app.route('/question/<int:question_id>/new_answer', methods=['POST'])
def add_answer(question_id):
    answer_id = file_handler.decode_file('answer.csv')
    with open('answer.csv', 'a') as file:
        file.write(str(int(answer_id[-1][0]) + 1) + ',')
        file.write(str(int(time.time())) + ',')
        file.write(str(0) + ',')    # Vote number
        file.write(str(question_id) + ',')
        file.write(str(file_handler.encode_string(request.form['answer'])) + ',')
        file.write(str('') + '\n')  # This will be the image
    return redirect('/list')


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
