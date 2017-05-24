import psycopg2


def user_datas():
    with open('user.txt') as file:
        data = file.read()
        data = data.split(',')
        return data


def fetch_database(query):
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

    # finally:
    #     if connection:
    #         connection.close()


def modify_database(query):
    try:
        data = user_datas()
        connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(query)  # fetchall ksizedése!!

    except psycopg2.DatabaseError as exception:
        print(exception)

    # finally:
    #     if connection:
    #         connection.close()


def all_questions():
    result = fetch_database("""SELECT * FROM question ORDER BY id;""")
    return result


def show_question(id):
    result = fetch_database("""SELECT title FROM question WHERE id={};""".format(id))
    return result


def update_question(title, id):
    result = modify_database("""UPDATE question SET title='{}' WHERE id={};""".format(title, id))
    return result


def display_question(id):
    result = fetch_database("""SELECT * FROM question WHERE id={}""".format(id))
    return result


def display_answer(id):
    result = fetch_database("""SELECT * FROM answer WHERE question_id={} ORDER BY id""".format(id))
    return result


def display_question_comment(id):
    result = fetch_database("""SELECT message FROM comment WHERE question_id={}""".format(id))
    return result


def display_answer_comment(answer_id):
    result = fetch_database(
        """SELECT answer_id, message, submission_time FROM comment WHERE answer_id={}""".format(answer_id))
    return result


def answer_comment_ids(id):
    result = fetch_database("""SELECT id FROM answer WHERE question_id={}""".format(id))
    q = []
    for item in result:
        q.append("".join(map(str, item)))
    return q


def delete_all_answer(id):
    result = modify_database("""DELETE FROM answer WHERE question_id={};""".format(id))
    return result


def delete_question_comment(question_id):
    result = modify_database("""DELETE FROM comment WHERE question_id={};""".format(question_id))
    return result


def delete_one_answer(answer_id):
    result = modify_database("""DELETE FROM answer WHERE id={};""".format(answer_id))
    return result


def delete_answer_comment(answer_id):
    result = modify_database("""DELETE FROM comment WHERE answer_id={};""".format(answer_id))
    return result


def delete_question(id):
    result = modify_database("""DELETE FROM question WHERE id={};""".format(id))
    return result


def add_new_anser(submission_time, vote_number, question_id, message, image):
    result = modify_database("""INSERT INTO answer(submission_time, vote_number, question_id, message, image) SELECT
                                '{}', {}, {}, '{}', '{}';""".format(submission_time, vote_number, question_id, message, image))


def handle_question_like(id, like_value):
    result = modify_database(
        """UPDATE question SET vote_number = vote_number + {} WHERE id={}""".format(like_value, id))


def handle_answer_like(id, like_value):
    result = modify_database(
        """UPDATE answer SET vote_number = vote_number + {} WHERE id={}""".format(like_value, id))
