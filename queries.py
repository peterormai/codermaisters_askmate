import psycopg2


def user_datas():
    """Read the nessecery information from the user_file to
    connect to the database, such as dbname, username, password
    """
    with open('user.txt') as file:
        data = file.read()
        data = data.split(',')
        return data


def fetch_database(query, tuple_parameters=None):
    """Connects to the database to retrieve data, then
    returns it.
    """
    try:
        data = user_datas()
        connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query, tuple_parameters)
        rows = cursor.fetchall()
        return rows

    except psycopg2.DatabaseError as exception:
        print(exception)

    finally:
        if conn:
            conn.close()


def modify_database(query, tuple_parameters=None):
    """Connects to the database then modifies the data
    without fetching anything.
    """
    try:
        data = user_datas()
        connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query, tuple_parameters)

    except psycopg2.DatabaseError as exception:
        print(exception)

    finally:
        if conn:
            conn.close()


def get_all_questions():
    """Returns all the questions"""
    return fetch_database("""SELECT * FROM question ORDER BY id;""")


def show_one_question(question_id):
    """Returns the currect question details that are to be changed by user"""
    return fetch_database("""SELECT title, message FROM question WHERE id=%s;""", (question_id,))


def get_question_details(question_id):
    """Returns all the details about a specific question"""
    return fetch_database("""SELECT * FROM question WHERE id=%s""", (question_id,))


def get_question_answers(question_id):
    """Returns all the answers to a specific question"""
    return fetch_database("""SELECT * FROM answer WHERE question_id=%s ORDER BY id""", (question_id,))


def get_question_comments(question_id):
    """Returns all the comments to a specific question"""
    return fetch_database("""SELECT message, id FROM comment WHERE question_id = %s""", (question_id,))


def get_answer_comments(answer_id):
    """Returns all the comments to a specific question-answer"""
    return fetch_database("""SELECT answer_id, message, submission_time, id
                         FROM comment WHERE answer_id = %s""", (answer_id,))


def get_answer_comment_ids(question_id):
    """Returns all the answer_comments IDs"""
    return fetch_database("""SELECT id FROM answer WHERE question_id = %s""", (question_id,))


def show_one_answer(answer_id):
    """Returns the currect answer details that are to be changed by user"""
    return fetch_database("""SELECT id, submission_time, message, image FROM answer WHERE id={};""".format(answer_id,))

# Database modifiers!


def submit_new_answer_comment(answer_id, message, submission_time):
    modify_database("""INSERT INTO comment(answer_id, message, submission_time)
                    SELECT {}, '{}', '{}';""".format(answer_id, message, submission_time))


def delete_question(question_id):
    """Deletes a question and all the associated answers and comments"""
    modify_database("""DELETE FROM question WHERE id = %s; """, (question_id,))


def delete_one_answer(answer_id):
    """Deletes a question based on ID from the database"""
    modify_database("""DELETE FROM answer WHERE id = %s; """, (answer_id,))


def add_new_answer(submission_time, vote_number, question_id, message, image):
    """Adds a new answer to a question"""
    modify_database("""INSERT INTO answer(submission_time, vote_number, question_id, message, image) VALUES
                    (%s, %s, %s, %s, %s); """, (submission_time, vote_number, question_id, message, image))


def submit_new_question(submission_time, view_number, vote_number, title, message, image):
    """Gets all the nessecery inputs from the user"""
    modify_database(
        """INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
        VALUES (%s, %s, %s, %s, %s, %s);""", (submission_time, view_number, vote_number, title, message, image))


def submit_new_question_comment(question_id, message, submission_time):
    modify_database("""INSERT INTO comment(question_id, message, submission_time)
                    VALUES (%s, %s, %s);""", (question_id, message, submission_time))


def update_question_query(title, message, question_id):
    """Updates the database with the edited question details"""
    modify_database("""UPDATE question SET title=%s, message=%s WHERE id=%s;""", (title, message, question_id))


def handle_question_like(question_id, like_value):
    """"Adds one or takes one from the question vote/like counter"""
    modify_database("""UPDATE question SET vote_number = vote_number + %s WHERE id = %s""", (like_value, question_id))


def handle_answer_like(answer_id, like_value):
    """"Adds one or takes one from the answer vote/like counter"""
    modify_database(
        """UPDATE answer SET vote_number = vote_number + %s WHERE id = %s""", (like_value, answer_id))


def get_latest_five_questions():
    """Returns with the details of the latest 5 question in descending order"""
    return fetch_database("""SELECT * FROM question ORDER BY id DESC LIMIT 5;""")


def delete_comment(comment_id):
    """Deletes a comment from answer or question comments"""
    modify_database("""DELETE FROM comment WHERE id=%s;""", (comment_id,))


def search_question_id(answer_id):
    """Searches the releted question id of the given answer id"""
    return fetch_database("""SELECT question_id FROM answer WHERE id=%s;""", (answer_id,))
