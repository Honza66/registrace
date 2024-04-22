import bcrypt
import psycopg2

def insert_user(email, password):
    connection = psycopg2.connect(
        dbname = 'bank',
        user = 'postgres',
        password = 'admin',
        host= 'localhost',
        port = '5432'
    )
    cur = connection.cursor()
    query = ''' INSERT INTO bank_user(email, password) VALUES(%s, %s)'''
    cur.execute(query, (email, password))
    connection.commit()
    connection.close()

insert_user('homer@sexymeda.com', 'admin')
