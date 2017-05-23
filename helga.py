import queries


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
