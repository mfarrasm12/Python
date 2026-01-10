from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from database import get_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")


# ================= AUTH =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].lower().strip()
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "user")
            )
            db.commit()
        except:
            db.close()
            return "Username already exists"

        db.close()
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].lower().strip()
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT password, role FROM users WHERE username = ?",
            (username,)
        )
        user = cur.fetchone()
        db.close()

        if user is None or user["password"] != password:
            return "Invalid login"

        session["user"] = username
        session["role"] = user["role"]

        # 🔑 ROLE-BASED REDIRECT
        if user["role"] == "admin":
            return redirect(url_for("adminDashboard"))
        else:
            return redirect(url_for("show_books"))

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# ================= ADMIN =================
@app.route("/admin")
def adminDashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("adminDashboard.html")


@app.route("/admin/add-book", methods=["POST"])
def add_book():
    if session.get("role") != "admin":
        return "Access Denied"

    name = request.form["book"].strip()
    qty = int(request.form["qty"])

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO books (name, quantity, borrowed) VALUES (?, ?, 0)",
        (name, qty)
    )
    db.commit()
    db.close()

    return redirect(url_for("adminDashboard"))


@app.route("/admin/show-library")
def show_library():
    if session.get("role") != "admin":
        return "Access Denied"

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    db.close()

    return render_template("showLibrary.html", library=books)


@app.route("/admin/borrowed")
def borrowed_records():
    if session.get("role") != "admin":
        return "Access Denied"

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM borrowed")
    records = cur.fetchall()
    db.close()

    return render_template("borrowedRecords.html", records=records)

@app.route("/admin/add-existing", methods=["POST"])
def add_existing_book():
    if session.get("role") != "admin":
        return "Access Denied"

    name = request.form["book"].strip()
    qty = int(request.form["qty"])

    if qty <= 0:
        return "Invalid quantity"

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT quantity FROM books WHERE name = ? COLLATE NOCASE",
        (name,)
    )
    book = cur.fetchone()

    if book is None:
        db.close()
        return "Book not found"

    cur.execute(
        "UPDATE books SET quantity = quantity + ? WHERE name = ? COLLATE NOCASE",
        (qty, name)
    )

    db.commit()
    db.close()

    return redirect(url_for("adminDashboard"))

@app.route("/admin/remove-book", methods=["POST"])
def remove_book():
    if session.get("role") != "admin":
        return "Access Denied"

    name = request.form["book"].strip()

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM books WHERE name = ? COLLATE NOCASE",
        (name,)
    )
    book = cur.fetchone()

    if book is None:
        db.close()
        return "Book not found"

    cur.execute(
        "DELETE FROM books WHERE name = ? COLLATE NOCASE",
        (name,)
    )

    # Also remove borrowed records of this book
    cur.execute(
        "DELETE FROM borrowed WHERE book = ? COLLATE NOCASE",
        (name,)
    )

    db.commit()
    db.close()

    return redirect(url_for("adminDashboard"))




# ================= BOOKS =================
@app.route("/books")
def show_books():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    db.close()

    return render_template("books.html", library=books)


# ================= BORROW =================
@app.route("/borrow", methods=["POST"])
def borrow_book():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    book = request.form["book"]
    qty = int(request.form["qty"])

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT quantity FROM books WHERE name = ? COLLATE NOCASE",
        (book,)
    )
    row = cur.fetchone()

    if row is None:
        db.close()
        return "Book not found"

    if qty > row["quantity"]:
        db.close()
        return "Not enough books"

    cur.execute(
        "UPDATE books SET quantity = quantity - ?, borrowed = borrowed + ? WHERE name = ? COLLATE NOCASE",
        (qty, qty, book)
    )

    cur.execute(
        "INSERT INTO borrowed (username, book, qty) VALUES (?, ?, ?) "
        "ON CONFLICT(username, book) DO UPDATE SET qty = qty + ?",
        (username, book, qty, qty)
    )

    db.commit()
    db.close()
    return redirect(url_for("show_books"))


# ================= RETURN =================
@app.route("/return", methods=["GET", "POST"])
def return_book():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":
        return render_template("return.html")

    username = session["user"]
    book = request.form["book"]
    qty = int(request.form["qty"])

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT qty FROM borrowed WHERE username = ? AND book = ? COLLATE NOCASE",
        (username, book)
    )
    record = cur.fetchone()

    if record is None or qty > record["qty"]:
        db.close()
        return "Invalid return"

    cur.execute(
        "UPDATE books SET quantity = quantity + ?, borrowed = borrowed - ? WHERE name = ? COLLATE NOCASE",
        (qty, qty, book)
    )

    cur.execute(
        "UPDATE borrowed SET qty = qty - ? WHERE username = ? AND book = ? COLLATE NOCASE",
        (qty, username, book)
    )

    cur.execute(
        "DELETE FROM borrowed WHERE qty = 0"
    )

    db.commit()
    db.close()

    return redirect(url_for("show_books"))


if __name__ == "__main__":
    app.run(debug=True)
