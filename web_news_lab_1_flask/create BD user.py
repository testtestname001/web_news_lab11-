import sqlite3

# Підключення до бази даних (створення нової бази, якщо її ще немає)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Створення таблиці users з полями id, login та password
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Закриття підключення
conn.commit()
conn.close()
