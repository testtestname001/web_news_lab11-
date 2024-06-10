import sqlite3

# Функція для вставки нового користувача
def insert_user(login, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
    conn.commit()
    conn.close()

# Вставка прикладів даних
insert_user('user1', 'password1')
insert_user('user2', 'password2')
