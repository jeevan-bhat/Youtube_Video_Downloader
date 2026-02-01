from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

DB = "database.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        status TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users VALUES (NULL, ?, ?)", (user, pwd))
            conn.commit()
        except:
            return "User already exists"
        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        data = cur.fetchone()
        conn.close()

        if data:
            session["user_id"] = data[0]
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    if request.method == "POST":
        task = request.form["task"]
        cur.execute(
            "INSERT INTO tasks VALUES (NULL, ?, 'Pending', ?)",
            (task, session["user_id"])
        )
        conn.commit()

    cur.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    )
    tasks = cur.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/toggle/<int:id>")
def toggle(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT status FROM tasks WHERE id=?", (id,))
    status = cur.fetchone()[0]

    new_status = "Done" if status == "Pending" else "Pending"
    cur.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, id))

    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)