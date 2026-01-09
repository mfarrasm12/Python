from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# ======== DATA STORAGE (TEMPORARY) =========
library = []
users = {
    "admin": {
        "password": "1234",
        "role": "admin",
        "borrowed": {}
    }
}


# ==================== ROUTES ====================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return "This is the about page"

@app.route("/admin")
def adminDashboard():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("adminDashboard.html", library=library)

@app.route("/admin/add-book", methods=["POST"])
def add_book():
    if session.get("role") != "admin":
        return "Access Denied"
    book = request.form["book"]
    qty = int(request.form["qty"])
    for item in library:
        if item["Book"].lower() == book.lower():
            return "This book already exists"
    library.append({
        "Book": book,
        "Quantity": qty,
        "MaxQuantity": qty,
        "borrowed": 0
    })
    return redirect(url_for("adminDashboard"))

@app.route("/admin/add-existing", methods=["POST"])
def add_exisiting_book():
    if session.get("role") != "admin":
        return "Access Denied"
    book = request.form["book"]
    add = int(request.form["qty"])
    if add <= 0:
        return "Invalid Quantity"
    for item in library:
        if item["Book"].lower() == book.lower():
            item["MaxQuantity"] += add
            item["Quantity"] += add
            return redirect(url_for("adminDashboard"))
    return "Book not found"

@app.route("/admin/remove-book", methods=["POST"])
def remove_book():
    if session.get("role") != "admin":
        return "Access denied"
    book = request.form["book"]
    for item in library:
        if item["Book"].lower() == book.lower():
            library.remove(item)
            return redirect(url_for("adminDashboard"))
    return "Book not found"

@app.route("/admin/show-library")
def show_library():
    if session.get("role") != "admin":
        return "Access Denied"
    return render_template("showLibrary.html", library=library)
    

@app.route("/admin/borrowed")
def borrowed_records():
    if session.get("role") != "admin":
        return "Access Denied"
    return render_template("borrowedRecords.html", users=users)


@app.route("/user")
def user():
    return "User Dashboard"

@app.route("/books")
def show_books():
    return render_template("books.html", library=library)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        if username in users:
            return "Username already exists"

        users[username] = {
            "password": password,
            "role": "user",
            "borrowed": {}
        }

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"]

        if username not in users:
            return "User not found"

        if users[username]["password"] != password:
            return "Wrong password"

        session["user"] = username   # 🔑 save login
        session["role"] = users[username]["role"]

        if session["role"] == "admin":
            return redirect(url_for("adminDashboard"))
        else:
            return redirect(url_for("show_books"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/borrow", methods=["POST"])
def borrow_book():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    book = request.form["book"]
    qty = int(request.form["qty"])
    found = False
    for item in library:
        if item["Book"] == book:
            found = True
            if qty > item["Quantity"]:
                return "Not enough books"

            item["Quantity"] -= qty
            item["borrowed"] += qty

            user_books = users[username]["borrowed"]
            user_books[book] = user_books.get(book, 0) + qty
            break
    if not found:
        return "Book not found"

    return redirect(url_for("show_books"))


@app.route("/return/<username>/<book>/<int:borrow>")
def return_book(username, book, borrow):
    username = username.lower()
    if username not in users:
        return "User not Found!"
    user_books = users[username]["borrowed"]
    if book not in user_books:
        return "You did not borrow this book"
    if borrow <= 0:
        return "Invalid quantity"
    if borrow > user_books[book]:
        return "Return quantity exceeds borrowed amount"
    for item in library:
        if item["Book"].lower() == book.lower():
            item["Quantity"] += borrow
            item["borrowed"] -= borrow
            break
    user_books[book] -= borrow
    if user_books[book] == 0:
        del user_books[book]
    return f"{username} returned {borrow} copy of {book}"

# ============== RUN APP =====================
if __name__ == "__main__":
    app.run(debug=True)
