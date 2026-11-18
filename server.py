from flask import Flask
import sqlite3

app = Flask(__name__)


# Database Banega
def create_db():
    conn = sqlite3.connect("echo.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


create_db()


@app.route("/")
def home():
    return "Echo Server Running"


# Register User
@app.route("/register/<username>/<password>")
def register(username, password):

    conn = sqlite3.connect("echo.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password) VALUES(?,?)",
        (username, password)
    )

    conn.commit()
    conn.close()

    return f"{username} Registered Successfully"


# Login User
@app.route("/login/<username>/<password>")
def login(username, password):

    conn = sqlite3.connect("echo.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return "Login Successful"

    return "Invalid Username or Password"


# Show All Users
@app.route("/users")
def users():

    conn = sqlite3.connect("echo.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    conn.close()

    return str(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)