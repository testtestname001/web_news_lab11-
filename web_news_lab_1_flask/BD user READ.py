import sqlite3

# Функція для отримання всіх користувачів
def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users

# Виведення всіх користувачів
for user in get_users():
    print(user)
