import psycopg2


def user_datas():
    """Read the nessecery information from the user_file to
    connect to the database, such as dbname, username, password
    """
    with open('user.txt') as file:
        data = file.read()
        data = data.split(',')
        return data


def fetch_database(query):
    """Connects to the database to retrieve data, then
    returns it.
    """
    try:
        data = user_datas()
        connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except psycopg2.DatabaseError as exception:
        print(exception)

    finally:
        if conn:
            conn.close()


def modify_database(query):
    """Connects to the database then modifies the data
    without fetching anything.
    """
    try:
        data = user_datas()
        connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)

    except psycopg2.DatabaseError as exception:
        print(exception)

    finally:
        if conn:
            conn.close()


def get_all_questions():
    """Returns all the questions"""
    return fetch_database("""SELECT * FROM question ORDER BY id;""")


def show_one_question(id):
    """Returns the currect question details that are to be changed by user"""
    return fetch_database("""SELECT title FROM question WHERE id={};""".format(id))


def update_question_query(title, message, id):
    """Updates the database with the edited question details"""
    modify_database("""UPDATE question SET title='{}', message='{}' WHERE id={};""".format(title, message, id))


def get_question_details(id):
    """Returns all the details about a specific question"""
    return fetch_database("""SELECT * FROM question WHERE id={}""".format(id))


def get_question_answers(id):
    """Returns all the answers to a specific question"""
    return fetch_database("""SELECT * FROM answer WHERE question_id={} ORDER BY id""".format(id))


def get_question_comments(id):
    """Returns all the comments to a specific question"""
    return fetch_database("""SELECT message FROM comment WHERE question_id = {}""".format(id))


def get_answer_comment(answer_id):
    """Returns all the comments to a specific question-answer"""
    return fetch_database("""SELECT answer_id, message, submission_time
                         FROM comment WHERE answer_id = {}""".format(answer_id))


def get_answer_comment_ids(id):
    """Returns all the answer_comments IDs"""
    answer_ids = fetch_database("""SELECT id FROM answer WHERE question_id = {}""".format(id))
    id_numbers = []
    for item in answer_ids:
        id_numbers.append("".join(map(str, item)))
    return id_numbers


def delete_one_answer(answer_id):
    """Deletes a question based on ID from the database"""
    modify_database("""DELETE FROM answer WHERE id = {}; """.format(answer_id))


def delete_answer_comment(answer_id):
    """Deletes a comment from an answer"""
    modify_database("""DELETE FROM comment WHERE answer_id = {}; """.format(answer_id))


def delete_question(id):
    """Deletes a question and all the associated answers and comments"""
    modify_database("""DELETE FROM question WHERE id = {}; """.format(id))


def add_new_answer(submission_time, vote_number, question_id, message, image):
    """Adds a new answer to a question"""
    modify_database("""INSERT INTO answer(submission_time, vote_number, question_id, message, image) SELECT
                    '{}', {}, {}, '{}', '{}'; """.format(submission_time, vote_number, question_id, message, image))


def handle_question_like(id, like_value):
    """"Adds one or takes one from the question vote/like counter"""
    modify_database("""UPDATE question SET vote_number = vote_number + {} WHERE id = {}""".format(like_value, id))


def handle_answer_like(id, like_value):
    """"Adds one or takes one from the answer vote/like counter"""
    modify_database(
        """UPDATE answer SET vote_number = vote_number + {} WHERE id = {}""".format(like_value, id))


def submit_new_question(submission_time, view_number, vote_number, title, message, image):
    """Gets all the nessecery inputs from the user"""
    modify_database(
        """INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
        SELECT '{}', {}, {}, '{}', '{}', '{}';"""
        .format(submission_time, view_number, vote_number, title, message, image)
    )


def view_counter(question_id):
    """Adds one to the view counter in the database"""
    modify_database("""UPDATE question SET view_number=view_number + 1 WHERE id={};""".format(question_id))


def submit_new_question_comment(question_id, message, submission_time):
    modify_database("""INSERT INTO comment(question_id, message, submission_time)
                    SELECT {}, '{}', '{}';""".format(question_id, message, submission_time))
