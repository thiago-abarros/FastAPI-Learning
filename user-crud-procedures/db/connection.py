import psycopg2

class PostgreSQLConnection:
    def __init__(self):
        self.dbname = 'mydatabase'
        self.user = 'postgres'
        self.password = 'postgres'
        self.host = 'db'
        self.port = '5432'

    def connect(self):
        try: 
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL: ", e)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        return cursor