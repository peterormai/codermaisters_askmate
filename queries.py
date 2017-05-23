import psycopg2


def user_datas():
    with open('user.txt') as file:
        data = file.read()
        data = data.split(',')
        return data


def fetch_database(func):
    def wrap():
        try:
            data = user_datas()
            connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
            conn = psycopg2.connect(connect_str)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(func())
            rows = cursor.fetchall()
            return rows

        except psycopg2.DatabaseError as exception:
            print(exception)

        # finally:
        #     if connection:
        #         connection.close()

    return wrap


def modify_database(func):
    def wrap():
        try:
            data = user_datas()
            connect_str = "dbname={0} user={0} host='localhost' password={1}".format(data[0], data[1])
            conn = psycopg2.connect(connect_str)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(func())
            rows = cursor.fetchall()
            return rows

        except psycopg2.DatabaseError as exception:
            print(exception)

        # finally:
        #     if connection:
        #         connection.close()

    return wrap


@fetch_database
def all_queistions():
    return """SELECT * FROM question;"""
