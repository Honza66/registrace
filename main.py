import bcrypt
import psycopg2
from tkinter import *



def password_to_hash(plain_password):
    try:
        password_bytes = plain_password.encode('utf-8')
        hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hash
    except Exception as error:
        print(f'Chyba při hashování hesla {error}')



def insert_user(email, password):
    try:
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
    except psycopg2.DatabaseError as error:
        print(f'Chyba databáze {error}')
    except Exception as error:
        print(f'obecná chyba {error}')


def get_hash_from_database(email):
    try:

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
    except psycopg2.DatabaseError as error:
        print(f'Chyba databáze {error}')
        return b''
    except Exception as error:
        print(f'obecná chyba {error}')
        return b''
    
def login_autentication(password,email):
    try:
        hash = get_hash_from_database(email)
        password_byte = bytes(password, encoding='utf-8')
        if hash == b'':
            result_label['text'] = 'Neplatné'
        else:
            if bcrypt.checkpw(password_byte, hash):
                result_label['text'] = 'Úspěšné přihlášení'
            else:
                result_label['text'] = 'Neplatné'
    except Exception as error:
        result_label['text'] = 'Chyba při ověřování'
        print(f'Chyba při ověřování {error}')
            
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

login_label = Label(text='Přihlášení')
login_label.grid(row=4, column=1)
emai_login_label = Label(text='email:')
emai_login_label.grid(row=5, column=0)
email_login_entry = Entry()
email_login_entry.grid(row=5, column=1)
password_login_label = Label(text='heslo:')
password_login_label.grid(row=6, column=0)
password_login_entry = Entry(show='*')
password_login_entry.grid(row=6, column=1)
login_button = Button(text='Přihlásit se',command=lambda:login_autentication(password_login_entry.get(), email_login_entry.get()))
login_button.grid(row=7, column=1)

result_label = Label()
result_label.grid(row=8, column=1)





root.mainloop()






    


    

