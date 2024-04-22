import bcrypt
import psycopg2

def password_to_hash(plain_password):
    password_bytes = plain_password.encode('utf-8')
    hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hash

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
    hash = password_to_hash(password)
    cur.execute(query, (email, hash))
    connection.commit()
    connection.close()

insert_user('sexymeda@aol.com','admin')

def get_hash_from_database(email):

    connection = psycopg2.connect(
        dbname = 'bank',
        user = 'postgres',
        password = 'admin',
        host= 'localhost',
        port = '5432'
    )
    cur = connection.cursor()
    query = ''' SELECT password FROM bank_user WHERE email = (%s)'''
    cur.execute(query, (email,))
    user_hash_password = cur.fetchone()
    connection.close()
    if user_hash_password:
        return bytes.fromhex(user_hash_password[0][2:])
    else:
        return b''

    

