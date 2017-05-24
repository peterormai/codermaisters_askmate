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
    result = modify_database("""UPDATE question SET title='{0}' WHERE id={1};""".format(title, id))
    return result


def display_question(id):
    result = fetch_database("""SELECT * FROM question WHERE id={}""".format(id))
    return result


def display_answer(id):
    result = fetch_database("""SELECT * FROM answer WHERE question_id={}""".format(id))
    return result


def display_question_comment(id):
    result = fetch_database("""SELECT message FROM comment WHERE question_id={}""".format(id))
    return result


def display_answer_comment(id):
    result = fetch_database("""SELECT message, submission_time FROM comment WHERE answer_id={}""".format(id))
    return result
