import queries

# xxgitbe mappa???


def show_question(id):
    """
    Redirect to the page of the question based on the received question ID as an argument.
    """
    data_list = file_handler.decode_file('database/question.csv')
    for item in data_list:
        if int(item[0]) == int(id):
            selected_question = item
    return render_template('update.html', selected_question=selected_question)


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
