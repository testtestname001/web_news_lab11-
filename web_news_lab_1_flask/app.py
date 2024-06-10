from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import os
from werkzeug.utils import secure_filename
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection(db_name='users.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection('posts.db')
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()
        if user:
            flash('Цей логін вже існує. Спробуйте інший.')
            return redirect(url_for('register'))
        conn.execute('INSERT INTO users (login, password) VALUES (?, ?)', (login, password))
        conn.commit()
        conn.close()
        flash('Реєстрація пройшла успішно!')
        return redirect(url_for('register'))
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            flash('Вхід успішний!')
            return redirect(url_for('index'))
        else:
            flash('Невірний логін або пароль. Спробуйте ще раз.')
    else:
        session.pop('_flashes', None)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Ви вийшли з системи.')
    return redirect(url_for('index'))

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if g.user is None:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            image_path = None
        conn = get_db_connection('posts.db')
        conn.execute('INSERT INTO posts (title, author, content, image_path) VALUES (?, ?, ?, ?)',
                     (title, g.user['login'], content, image_path))
        conn.commit()
        conn.close()
        flash('Пост успішно створений!')
        return redirect(url_for('index'))
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('new_post.html', current_time=current_time)


@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    if g.user is None:
        return redirect(url_for('login'))
    conn = get_db_connection('posts.db')
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join('static/uploads', filename)
            conn.execute('UPDATE posts SET title = ?, content = ?, image_path = ? WHERE id = ?',
                         (title, content, image_path, id))
        else:
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                         (title, content, id))
        conn.commit()
        conn.close()
        flash('Пост успішно оновлений!')
        return redirect(url_for('index'))
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('edit_post.html', post=post, current_time=current_time)



@app.route('/post/delete/<int:id>', methods=['POST'])
def delete_post(id):
    if g.user is None:
        return redirect(url_for('login'))
    
    conn = get_db_connection('posts.db')
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    
    if post is None:
        flash('Пост не знайдено.')
        return redirect(url_for('index'))
    
    if g.user['login'] != post['author']:
        flash('Ви не маєте права видаляти цей пост.')
        return redirect(url_for('index'))
    
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Пост успішно видалений!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
