import sqlite3

conn = sqlite3.connect('helper.db')
c = conn.cursor()


def add_user_db(user_id, username, first_name, last_name):
    c.execute('''SELECT user_id FROM user_inf''')
    user_list = []
    for i in c.fetchall():
        user_list += list(i)
    if user_id not in user_list:
        c.execute('''INSERT INTO user_inf(user_id, username, first_name, last_name) VALUES(?,?,?,?)''',
                  (user_id, username, first_name, last_name))
        conn.commit()
    else:
        print('Уже зарегистрирован.')


def select_idea(user_id):
    c.execute('''SELECT user_idea FROM ideas WHERE user_id=?''', (user_id,))
    ideas = c.fetchall()
    return ideas


def insert_idea(user_id, user_date, idea):
    c.execute('''INSERT INTO ideas VALUES(?,?,?)''', (user_id, user_date, idea))
    conn.commit()


def delete_idea_db(key):
    c.execute('''DELETE FROM ideas WHERE user_idea=?''', key)
    conn.commit()


def select_film(user_id):
    c.execute('''SELECT film FROM films WHERE user_id=?''', (user_id,))
    films = c.fetchall()
    return films


def insert_film(user_id, user_date, film):
    c.execute('''INSERT INTO films VALUES(?,?,?)''', (user_id, user_date, film))
    conn.commit()


def delete_film_db(key):
    c.execute('''DELETE FROM films WHERE film=?''', key)
    conn.commit()


def select_todo(user_id):
    c.execute('''SELECT to_do FROM to_do_list WHERE user_id=?''', (user_id,))
    todo = c.fetchall()
    return todo


def insert_todo(user_id, user_date, new_todo):
    c.execute('''INSERT INTO to_do_list VALUES(?,?,?)''', (user_id, user_date, new_todo))
    conn.commit()


def delete_todo_db(key):
    c.execute('''DELETE FROM to_do_list WHERE to_do=?''', key)
    conn.commit()


def select_num_name(user_id):
    c.execute('''SELECT contact_name, number FROM contacts WHERE user_id=?''', (user_id,))
    contact = c.fetchall()
    return contact


def select_contact(user_id):
    c.execute('''SELECT number FROM contacts WHERE user_id=?''', (user_id,))
    contacts = c.fetchall()
    return contacts


def insert_contact(user_id, contact_name, cont_num_form, user_date):
    c.execute('''INSERT INTO contacts VALUES(?,?,?,?)''', (user_id, contact_name, cont_num_form, user_date))
    conn.commit()


def delete_contact_db(key):
    c.execute('''DELETE FROM contacts WHERE number=?''', key)
    conn.commit()


def select_link(user_id):
    c.execute('''SELECT link FROM links WHERE user_id=?''', (user_id,))
    links = c.fetchall()
    return links


def insert_link(user_id, user_date, link):
    c.execute('''INSERT INTO links VALUES(?,?,?)''', (user_id, user_date, link))
    conn.commit()


def delete_link_db(key):
    c.execute('''DELETE FROM links WHERE link=?''', key)
    conn.commit()


def select_book(user_id):
    c.execute('''SELECT book_name, author FROM books WHERE user_id=?''', (user_id,))
    books = c.fetchall()
    return books


def select_book_name(user_id):
    c.execute('''SELECT book_name FROM books WHERE user_id=?''', (user_id,))
    b = c.fetchall()
    return b


def insert_book(user_id, author, book_name, user_date):
    c.execute('''INSERT INTO books VALUES (?,?,?,?)''', (user_id, author, book_name, user_date))
    conn.commit()


def delete_book_db(key):
    c.execute('''DELETE FROM books WHERE book_name=?''', key)
    conn.commit()
