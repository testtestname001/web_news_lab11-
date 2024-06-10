import sqlite3

def create_posts_db():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    # Створення таблиці для постів
    cursor.execute('''
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("База даних для постів успішно створена.")

if __name__ == '__main__':
    create_posts_db()
