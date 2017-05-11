from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import time
import file_handler
import base64


app = Flask(__name__)

# Main page


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def list_questions():
    """
    List all questions from the database.
    """
    data_list = file_handler.decode_file('database/question.csv')
    title = "Cödermeisters's ask-mate"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    return render_template('index.html', title=title, data_list=data_list, top_menu=top_menu)


@app.route("/sortby", methods=['POST'])
def sort_by():
    """
    Sort the list by indicators.
    """
    title = "Super Sprinter 3000"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    data_list = file_handler.list_of_files('database/question.csv')
    search_key = str(request.form['sortby'])
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
    for lines in data_list:
        lines[1] = time.ctime(int(lines[1]))
        lines[4] = base64.urlsafe_b64decode(str.encode(lines[4])).decode()
        lines[5] = base64.urlsafe_b64decode(str.encode(lines[5])).decode()
        lines[6] = base64.urlsafe_b64decode(str.encode(lines[6])).decode()
    return render_template('index.html', data_list=data_list, title=title, top_menu=top_menu)


@app.route("/like/<int:id>/<int:like_value>/<from_page>", methods=['GET'])
def handle_like(id, like_value, from_page):
    """Change the number of likes according to user.
    Receives three arguments:
        - id: ID row
        - like_value: number of current likes (default is set to ‘0’)
        - from_page: name of the current page
    Overwrites old data with new data and redirects to the current page.
    """
    data_list = file_handler.list_of_files('database/question.csv')
    for item in data_list:
        if int(item[0]) == int(id):
            if int(like_value) == 1:
                item[3] = str(int(item[3]) + 1)
            elif int(like_value) == 0:
                item[3] = str(int(item[3]) - 1)
    file_handler.write_to_file('database/question.csv', data_list)
    if from_page == 'display':
        return redirect("/question/" + str(id))
    else:
        return redirect("/list")


@app.route("/like/<int:answer_id>/<from_page>/<int:like_value>", methods=['GET'])
def answer_handle_like(answer_id, from_page, like_value):
    """Change the number of likes according to user.
    Receives two arguments:
        - answer_id
        - like_value: number of current likes (default is set to ‘0’)
    Overwrites old data with new data and redirects to the current page.
    """
    data_list = file_handler.list_of_files('database/answer.csv')
    for item in data_list:
        if int(item[0]) == int(answer_id):
            if int(like_value) == 1:
                item[2] = str(int(item[2]) + 1)
            elif int(like_value) == 0:
                item[2] = str(int(item[2]) - 1)
            question = item
            break
    file_handler.write_to_file('database/answer.csv', data_list)
    return redirect("/question/" + str(question[3]))


@app.route("/question/<int:id>/edit", methods=["GET"])
def show_question(id):
    """
    Redirect to the page of the question based on the received question ID as an argument.
    """
    data_list = file_handler.decode_file('database/question.csv')
    for item in data_list:
        if int(item[0]) == int(id):
            selected_question = item
    return render_template('update.html', selected_question=selected_question)


@app.route("/question/<int:id>/edit", methods=["POST"])
def update_question(id):
    """
    Redirect to a page where the user can change the question title and description.
    """
    selected_question = request.form["question_update"]
    selected_question = file_handler.encode_string(selected_question)
    data_list = file_handler.list_of_files('database/question.csv')
    for item in data_list:
        if int(item[0]) == int(id):
            item[4] = selected_question
    data_list = file_handler.write_to_file('database/question.csv', data_list)
    return redirect("/list")


@app.errorhandler(404)
def page_not_found(e):
    """
    Error handling for wrong DNS address request.
    """
    return render_template('404.html')


# Display question


@app.route('/question/<int:question_id>')
def question_display(question_id):
    """
    Display the question with all the answers below.
    Given the right argument, the related question will be displayed with answers to it.
    """
    webpage_title = 'Question & answers'
    question_list = file_handler.decode_file('database/question.csv')
    selected_question = []
    for item in question_list:
        if int(item[0]) == question_id:
            selected_question = item
            item[2] = str(int(item[2]) + 1)
    answer_list = file_handler.decode_file('database/answer.csv')
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
    """
    Given the right argument, the related answer will be removed from the database permanently. 
    """
    question_id = 0
    answer_list = file_handler.list_of_files('database/answer.csv')
    for item in answer_list:
        if int(item[0]) == answer_id:
            answer_list.remove(item)
            question_id = item[3]
    file_handler.write_to_file('database/answer.csv', answer_list)
    question_url = '/question/' + str(question_id)
    return redirect(question_url)


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    """
    Given the right argument, the related question will be removed with all the answers from the database permanently. 
    """
    question_list = file_handler.list_of_files('database/question.csv')
    for item in question_list:
        if int(item[0]) == question_id:
            question_list.remove(item)
    file_handler.write_to_file('database/question.csv', question_list)
    answer_list = file_handler.list_of_files('database/answer.csv')
    new_answer_list = []
    for item in answer_list:
        if int(item[3]) != question_id:
            new_answer_list.append(item)
    file_handler.write_to_file('database/answer.csv', new_answer_list)
    return redirect('/')


# New answer


@app.route('/question/<int:question_id>/new_answer')
def new_answer(question_id):
    """
    The user is able to answer any question.
    One argument: specific question ID of the question.
    """
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
    """
    Create a new answer by the user input to a specific question.
    """
    answer_id = file_handler.decode_file('database/answer.csv')
    vote_number = 0
    picture_url = request.form["picture"]
    picture_encoded = file_handler.encode_string(request.form["picture"])
    if len(request.form['answer']) < 10:
        return redirect('/question/' + str(question_id) + '/new_answer')
    else:
        with open('database/answer.csv', 'a') as file:
            if answer_id:
                answer_id = int(answer_id[-1][0])
            else:
                answer_id = -1
            file.write(str(answer_id + 1) + ',')
            file.write(str(int(time.time())) + ',')
            file.write(str(vote_number) + ',')
            file.write(str(question_id) + ',')
            file.write(str(file_handler.encode_string(request.form['answer'])) + ',')
            file.write(str(picture_encoded) + '\n')
        return redirect('/list')

# New question


@app.route("/new_question")
def question():
    """
    Show new_question page.
    """
    return render_template("new_question.html")


@app.route("/new_question", methods=["POST"])
def submit_new_question():
    """Takes a new question and description from user and encrypts it.
    Receives data fromm the user input, uses BASE64 encryption for title and description.
    Set by default an ID number, creation time, view and like number and save it as a .csv file.
    """
    new_question_title = request.form["new_question"]
    if len(new_question_title) < 10:
        return redirect('new_question')
    else:
        new_question_title_encoded = file_handler.encode_string(new_question_title)
        new_question_message = request.form["new_question_long"]
        new_question_message_encoded = file_handler.encode_string(new_question_message)
        picture_url = request.form["picture"]
        picture_encoded = file_handler.encode_string(picture_url)
        count_view = 0
        count_like = 0
        question_time = (int(time.time()))
        data_list = file_handler.list_of_files("database/question.csv")

        if len(data_list) > 0:
            question_id = str(int(data_list[-1][0]) + 1)
        else:
            question_id = 0

        with open("database/question.csv", "a") as file:
            file.write(str(question_id) + ",")
            file.write(str(question_time) + ",")
            file.write(str(count_view) + ",")
            file.write(str(count_like) + ",")
            file.write(str(new_question_title_encoded) + ",")
            file.write(str(new_question_message_encoded) + ",")
            file.write(str(picture_encoded) + "\n")

        return redirect('/question/' + str(question_id))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
