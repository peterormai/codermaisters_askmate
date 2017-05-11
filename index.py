from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import csv
import time
import file_handler
import base64


app = Flask(__name__)

# Main page


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def list_questions():
    """ lists all the questions from the database
    """
    with open('database/question.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
    for item in data_list:
        item[1] = time.strftime("%D %H:%M", time.localtime(int(item[1])))
    title = "Cödermeisters's ask-mate"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    return render_template('index.html', title=title, data_list=data_list, top_menu=top_menu)


@app.route("/sortby", methods=['POST'])
def sort_by():
    """ sorts the list based on different criterias
    """
    title = "Super Sprinter 3000"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    search_key = str(request.form['sortby'])
    with open('database/question.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        sort_value = str(request.form['sortby'])
        if search_key == 'ID':
            data_list = sorted(data_list, key=lambda x: x[0])
        elif search_key == 'created':
            data_list = sorted(data_list, key=lambda x: str(x[1]))
        elif search_key == 'views':
            data_list = sorted(data_list, key=lambda x: int(x[2]))
        elif search_key == 'votes':
            data_list = sorted(data_list, key=lambda x: int(x[3]))
        elif search_key == 'title':
            data_list = sorted(data_list, key=lambda x: str(x[4]))
        for item in data_list:
            item[1] = time.strftime("%D %H:%M", time.localtime(int(item[1])))
    return render_template('index.html', data_list=data_list, title=title, top_menu=top_menu)


@app.route("/like/<int:id>/<int:like_value>", methods=['GET'])
def handle_like(id, like_value):
    """ receives two inputs, id and likevalue, then
    changes the quantity of likes based on the ID row, based on likevalue.
    """
    with open('database/question.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                if int(like_value) == 1:
                    item[3] = int(item[3]) + 1
                elif int(like_value) == 0:
                    item[3] = int(item[3]) - 1

    with open('database/question.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_list)
    return redirect("/list")


@app.route("/question/<int:id>/edit", methods=["GET"])
def show_question(id):
    """ receives an ID from the browser then redirects to a new page where the
    question gets displayed
    """
    with open('database/question.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                selected_question = item
        return render_template('update.html', selected_question=selected_question)


@app.route("/question/<int:id>/edit", methods=["POST"])
def update_question(id):
    """ The user can change the question title and description on this page
    """
    selected_question = request.form["question_update"]
    with open('database/question.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                item[4] = selected_question.replace("\r\n", " ")

    with open('database/question.csv', 'w') as file:
        for item in data_list:
            file.write(",".join(item) + "\n")
    return redirect("/list")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# Display question


@app.route('/question/<int:question_id>')
def question_display(question_id):
    webpage_title = 'Question & answers'
    with open('database/question.csv') as question:
        question_list = question.read().splitlines()
        question_list = [item.split(",") for item in question_list]
        selected_question = []
        for item in question_list:
            if int(item[0]) == question_id:
                selected_question = item
    with open('database/answer.csv') as answer:
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
    with open('database/answer.csv') as answer:
        answer_list = answer.read().splitlines()
        answer_list = [item.split(",") for item in answer_list]
        for item in answer_list:
            if int(item[0]) == answer_id:
                answer_list.remove(item)
                question_id = item[3]
    with open('database/answer.csv', 'w') as file:
        for item in answer_list:
            answers = ','.join(item)
            file.write(str(answers) + '\n')
    question_url = '/question/' + str(question_id)
    return redirect(question_url)


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    with open('database/question.csv') as question:
        question_list = question.read().splitlines()
        question_list = [item.split(",") for item in question_list]
        for item in question_list:
            if int(item[0]) == question_id:
                question_list.remove(item)
    with open('database/question.csv', 'w') as file:
        for item in question_list:
            questions = ','.join(item)
            file.write(str(questions) + '\n')
    with open('database/answer.csv') as answer:
        answer_list = answer.read().splitlines()
        answer_list = [item.split(",") for item in answer_list]
        new_answer_list = []
        for item in answer_list:
            if int(item[3]) != question_id:
                new_answer_list.append(item)
    with open('database/answer.csv', 'w') as file:
        for item in new_answer_list:
            answers = ','.join(item)
            file.write(str(answers) + '\n')
    return redirect('/')


# New answer


@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    question_list = file_handler.decode_file('database/question.csv')
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
    answer_id = file_handler.decode_file('database/answer.csv')
    with open('database/answer.csv', 'a') as file:
        file.write(str(int(answer_id[-1][0]) + 1) + ',')
        file.write(str(int(time.time())) + ',')
        file.write(str(0) + ',')    # Vote number
        file.write(str(question_id) + ',')
        file.write(str(file_handler.file_handler.encode_string(request.form['answer'])) + ',')
        file.write(str('') + '\n')  # This will be the image
    return redirect('/list')


# New question


@app.route("/new_question")
def question():
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def submit_new_question():
    new_question_title = request.form["new_question"]
    new_question_title_encoded = file_handler.encode_string(new_question_title)
    new_question_message = request.form["new_question_long"]
    new_question_message_encoded = file_handler.encode_string(new_question_message)
    picture_url = request.form["picture"]
    count_view = 0
    count_like = 0
    question_time = time.time()

    with open("database/question.csv", "r") as file:
        data_list = file.read().splitlines()
        data_list = [item.split(",") for item in data_list]
        if len(data_list) > 0:
            question_id = str(int(data_list[-1][0]) + 1)
        else:
            question_id = 0

    with open("database/question.csv", "a") as file:
        file.write(str(question_id) + ",")
        file.write(str(question_time) + ",")
        file.write(str(count_view) + ",")
        file.write(str(count_like) + ",")
        file.write(str(new_question_title_encoded)[2:-1] + ",")
        file.write(str(new_question_message_encoded)[2:-1] + ",")
        file.write(str(picture_url + "\n"))

    return render_template("new_question.html")
    # redirect to Peti's page at the end with ...question/current_id !!!!!! ****


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
