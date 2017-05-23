import queries
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


def list_questions():
    """
    List all questions from the database.
    """
    data_list = queries.all_questions()
    title = "Cödermeisters's ask-mate"
    top_menu = ['ID', 'Created at', 'Views', 'Votes', 'Title', 'Edit', 'Delete', "Like", "Dislike"]
    return render_template('index.html', title=title, data_list=data_list, top_menu=top_menu)


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
