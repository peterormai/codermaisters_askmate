import queries


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
