import psycopg2


def main():
    try:
        # setup connection string
        connect_str = "dbname='yourdatabasename' user='yoursername' host='localhost' password='yourpassword'"
        
        # use our connection values to establish a connection
        connection = psycopg2.connect(connect_str)
        
        # set autocommit option, to do every query when we call it
        connection.autocommit = True
        
        # create a psycopg2 (client side) cursor that can execute queries
        cursor = connection.cursor()
        
        # removing the test table if it already exists
        cursor.execute("DROP TABLE IF EXISTS test;")
        
        # Execute a command: this creates a new table
        cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no more SQL injections!)
        cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

        # Query the database and obtain data as Python objects
        cursor.execute("SELECT * FROM test;")
        rows = cursor.fetchall()
        print(rows)

        # Close communication with the database
        cursor.close()

    except psycopg2.DatabaseError as exception:
        print(exception)

    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    main()
