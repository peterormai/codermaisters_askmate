from flask import Flask, render_template, request, redirect
import time
import base64
app = Flask(__name__)


def list_of_file(filename):
    with open(filename) as file:
        filelist = [line.split(',') for line in file.read().splitlines()]
    if filename == 'answer.csv':
        for lines in filelist:
            lines[1] = time.ctime(int(lines[1]))
            lines[4] = base64.b64decode(str.encode(lines[4])).decode()
    elif filename == 'question.csv':
        for lines in filelist:
            lines[1] = time.ctime(int(lines[1]))
            lines[4] = base64.b64decode(str.encode(lines[4])).decode()
            lines[5] = base64.b64decode(str.encode(lines[5])).decode()
    else:
        pass
    return filelist


@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    question_list = list_of_file('question.csv')
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
    answer_id = list_of_file('answer.csv')
    with open('answer.csv', 'a') as file:
        file.write(str(int(answer_id[-1][0]) + 1) + ',')
        file.write(str(int(time.time())) + ',')
        file.write(str(0) + ',')    # Vote number
        file.write(str(question_id) + ',')
        file.write(str(base64.b64encode(str.encode(request.form['answer']).decode())) + ',')
        file.write(str('') + '\n')  # This will be the image
    return redirect('/list')


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
