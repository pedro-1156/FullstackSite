from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        nome = request.form['nome']
        email = request.form['email']

        cursor.execute(
            "INSERT INTO pessoas (nome, email) VALUES (?, ?)",
            (nome, email)
        )

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pessoas")
    pessoas = cursor.fetchall()
    conn.close()

    return render_template("index.html", pessoas=pessoas)

if __name__ == '__main__':
    app.run(debug=True)
