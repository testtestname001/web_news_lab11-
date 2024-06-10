import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Видалення всіх записів з таблиці users
c.execute("DELETE FROM users")

# Підтвердження змін
conn.commit()

# Закриття підключення
conn.close()

print("Всі користувачі були успішно видалені.")
