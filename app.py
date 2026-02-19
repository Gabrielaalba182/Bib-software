from flask import Flask, render_template, request, redirect
import sqlite3
from database import init_db

app = Flask(__name__)

init_db()

def get_connection():
    conn = sqlite3.connect("biblioteca.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("index.html", books=books)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        conn = get_connection()
        conn.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_book.html")

@app.route("/borrow/<int:id>")
def borrow_book(id):
    conn = get_connection()
    conn.execute("UPDATE books SET available = 0 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/return/<int:id>")
def return_book(id):
    conn = get_connection()
    conn.execute("UPDATE books SET available = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
