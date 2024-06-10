import sqlite3

def add_user(login, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Перевірка, чи існує користувач з таким логіном
    c.execute("SELECT * FROM users WHERE login=?", (login,))
    existing_user = c.fetchone()

    if existing_user:
        print("Користувач з таким логіном вже існує.")
    else:
        # Додавання нового користувача
        c.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
        conn.commit()
        print("Користувач з логіном '{}' був успішно доданий.".format(login))

    conn.close()

# Приклад використання функції
add_user('user1', 'password1')
add_user('user2', 'password2')
add_user('user1', 'password3')  # Повинен вивести повідомлення про існуючого користувача
