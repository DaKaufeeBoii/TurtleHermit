from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    conn= get_db_connection()
    cur= conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)");
    conn.commit()
    conn.close()

# def create_movies_table():
#     conn= get_db_connection()
#     cur= conn.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, image TEXT NOT NULL)");
#     conn.commit()
#     # cur.execute("INSERT INTO movies(title, description, image) VALUES('Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.', 'inception.jpg'), ('The Dark Knight', 'Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice when the Joker emerges.', 'dark_knight.jpg'), ('Avengers Endgame', 'After the devastating events of Infinity War, the Avengers assemble once more to undo Thanos actions and restore balance to the universe.', 'endgame.jpg'), ('The Matrix', 'A hacker learns about the true nature of his reality and his role in the war against its controllers.', 'matrix.jpg');")
#     # conn.commit()
#     conn.close()

# Routes
@app.route('/')
def home():
    conn = get_db_connection()
    # movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return render_template('home.html')#, movies=movies)

@app.route("/admin")
def admin():
    conn=get_db_connection()
    cur=conn.cursor()
    cur.execute('SELECT* FROM users')
    data= cur.fetchall()
    return render_template('admin.html', users=data)
    print(data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect('/')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except:
            return "Username already exists"
    return render_template('signup.html')

@app.route('/trailers')
def trailers():
    conn= get_db_connection()
    conn.close()
    return render_template('trailers.html')

if __name__ == '__main__':
    get_db_connection()
    # create_movies_table()
    create_users_table()
    app.run(debug=True)
