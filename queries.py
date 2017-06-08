import psycopg2
import random


def user_datas():
    """Read the nessecery information from the user_file to
    connect to the database, such as dbname, username, password
    """
    with open('user.txt') as file:
        data = file.read()
        data = data.split(',')
        return data


def fetch_database(query, tuple_parameters=None, fetch='all'):
    """Connects to the database to retrieve data, then
    returns it.
    First parameter: query
    Second parameter: parameters which you want to insert into your query, use tupple type
    Third parameter: fetch type, one or all, use string type
    """
    try:
        data = user_datas()
        connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query, tuple_parameters)
        if fetch == 'all':
            rows = cursor.fetchall()
        elif fetch == 'one':
            rows = cursor.fetchone()
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


def submit_new_answer_comment(answer_id, message, submission_time, user_id):
    """Creates a new row in users table based on the registration form"""
    modify_database("""INSERT INTO comment(answer_id, message, submission_time, user_id)
                    VALUES(%s, %s, %s, %s);""", (answer_id, message, submission_time, user_id))


def register_new_user(user_name, password, email, registration_time):
    modify_database("""INSERT INTO users(username, password, email, registration_time)
                    SELECT '{}', '{}', '{}', '{}';""".format(user_name, password, email, registration_time))


def delete_question(question_id):
    """Deletes a question and all the associated answers and comments"""
    modify_database("""DELETE FROM question WHERE id = %s; """, (question_id,))


def delete_one_answer(answer_id):
    """Deletes a question based on ID from the database"""
    modify_database("""DELETE FROM answer WHERE id = %s; """, (answer_id,))


def add_new_answer(submission_time, vote_number, question_id, message, image, user_id):
    """Adds a new answer to a question"""
    modify_database("""INSERT INTO answer(submission_time, vote_number, question_id, message, image, user_id) VALUES
                    (%s, %s, %s, %s, %s, %s); """, (submission_time, vote_number, question_id, message, image, user_id))


def submit_new_question(submission_time, view_number, vote_number, title, message, image, user_id):
    """Gets all the nessecery inputs from the user"""
    modify_database(
        """INSERT INTO question(submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s);""",
        (submission_time, view_number, vote_number, title, message, image, user_id))


def submit_new_question_comment(question_id, message, submission_time, user_id):
    modify_database("""INSERT INTO comment(question_id, message, submission_time, user_id)
                    VALUES (%s, %s, %s, %s);""", (question_id, message, submission_time, user_id))


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


def get_all_users():
    """Shows all the registered users."""
    return fetch_database("""SELECT username, email, registration_time, role FROM users;""")

# #######################USER AUTHENTICATION########################


def check_user(username, password):
    return fetch_database(
        """SELECT role FROM users WHERE username=%s AND password=%s;""", (username, password), 'one')


def creator_username(type_, id):
    try:
        return fetch_database("""SELECT username FROM users
                            LEFT JOIN {0} ON users.id={0}.user_id
                            WHERE {0}.id=%s;""".format(type_), (id,), 'one')[0]
    except TypeError:
        return None


def creator_id(creator_username):
    return fetch_database("""SELECT id FROM users WHERE username=%s;""", (creator_username,), 'one')[0]


def password_generator(length):
    char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@£$%^&*().,?0123456789'
    password = ''
    for char in range(length):
        password += random.choice(char_set)
    return password


def password_recovery(email):
    password = password_generator(10)
    modify_database("""UPDATE users SET password=%s WHERE email=%s;""", (password, email))
    return password
