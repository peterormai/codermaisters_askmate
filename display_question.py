from flask import Flask, render_template, redirect
import index


app = Flask(__name__)


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def main_page():
    return index.list_questions()


@app.route('/question/<int:question_id>')
def question_display(question_id):
    webpage_title = 'Question & answers'
    with open('question.csv') as question:
        question_list = question.read().splitlines()
        question_list = [item.split(",") for item in question_list]
        selected_question = []
        for item in question_list:
            if int(item[0]) == int(question_id):
                selected_question = item
    with open('answer.csv') as answer:
        answer_list = answer.read().splitlines()
        answer_list = [item.split(",") for item in answer_list]
        related_answers = []
        for item in answer_list:
            if int(item[3]) == int(question_id):
                related_answers.append(item)
        return render_template('question_display.html',
                               question=selected_question,
                               answers=related_answers,
                               webpage_title=webpage_title)


@app.route('/answer/<int:answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    question_id = 0
    with open('answer.csv') as answer:
        answer_list = answer.read().splitlines()
        answer_list = [item.split(",") for item in answer_list]
        for item in answer_list:
            if int(item[0]) == int(answer_id):
                answer_list.remove(item)
                question_id = item[3]
    with open('answer.csv', 'w') as file:
        for item in answer_list:
            answers = ','.join(item)
            file.write(str(answers) + '\n')
    question_url = '/question/' + str(question_id)
    return redirect(question_url)


@app.route('/question/<int:id>/delete', methods=['POST'])
def delete_question(id):
    with open('question.csv') as question:
        question_list = question.read().splitlines()
        question_list = [item.split(",") for item in question_list]
        for item in question_list:
            if int(item[0]) == int(id):
                question_list.remove(item)
    with open('question.csv', 'w') as file:
        for item in question_list:
            questions = ','.join(item)
            file.write(str(questions) + '\n')
    with open('answer.csv') as answer:
        answer_list = answer.read().splitlines()
        answer_list = [item.split(",") for item in answer_list]
        new_answer_list = []
        for item in answer_list:
            if int(item[3]) != int(id):
                new_answer_list.append(item)
    with open('answer.csv', 'w') as file:
        for item in new_answer_list:
            answers = ','.join(item)
            file.write(str(answers) + '\n')
    return redirect('/')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()

# GIT!!!!!!!!
# unix base 64?
# több functionbe?
# kérdés url nem szűnik meg
# követelményeket megnézni, feladatot újraolvasni, git!!!!!
# HOLNAP: szebb html megjelenítés, clean code, követelményeknek megfelelő változtatások
# hibakezelés, 404, vessző, enter
# answe_id jav
# id int??
