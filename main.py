import bcrypt
import psycopg2
from tkinter import *



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
    
def login_autentication(password,email):
    hash = get_hash_from_database(email)
    password_byte = bytes(password, encoding='utf-8')
    if hash == b'':
        print('neplatné')
    else:
        if bcrypt.checkpw(password_byte, hash):
            print('Úspěšné přihlášení')
        else:
            print('neplatné')
            
root = Tk()
root.title('Registrace a přihlášení')
root.geometry('300x300')
root.resizable(False, False)

registration_label = Label( text='Registrace')
registration_label.grid(row=0, column=1)
email_label = Label(text='email:')
email_label.grid(row=1, column= 0 )
email_entry = Entry()
email_entry.grid(row=1, column=1)
password_label = Label(text='heslo:')
password_label.grid(row=2, column=0)
password_entry = Entry(show='*')
password_entry.grid(row=2, column=1)
registration_button = Button(text='Zaregistrovat', command= lambda:insert_user(email_entry.get(), password_entry.get()))
registration_button.grid(row=3, column=1)




root.mainloop()






    


    

