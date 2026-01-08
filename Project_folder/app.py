from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# ======== DATA STORAGE (TEMPORARY) =========
library = []
library.append({
    "Book": "Python Basics",
    "Quantity": 5,
    "Borrowed": 0,
    "MaxQuantity": 5
})
users= {}

# ==================== ROUTES ====================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return "This is the about page"

@app.route("/admin")
def admin():
    return "Admin Dashboard"

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

    for item in library:
        if item["Book"] == book:
            if qty > item["Quantity"]:
                return "Not enough books"

            item["Quantity"] -= qty
            item["Borrowed"] += qty

            user_books = users[username]["borrowed"]
            user_books[book] = user_books.get(book, 0) + qty

            break

    return redirect(url_for("show_books"))


@app.route("/return/<username>/<book>/<int:borrow>")
def return_book(username, book, borrow):
    username = username.lower()
    if username not in users:
        return "User not Found!"
    user_books = users[username]["Borrowed"]
    if book not in user_books:
        return "You did not borrow this book"
    if borrow <= 0:
        return "Invalid quantity"
    if borrow > user_books[book]:
        return "Return quantity exceeds borrowed amount"
    for item in library:
        if item["Book"].lower() == book.lower():
            item["Quantity"] += borrow
            item["Borrowed"] -= borrow
            break
    user_books[book] -= borrow
    if user_books[book] == 0:
        del user_books[book]
    return f"{username} returned {borrow} copy of {book}"

# ============== RUN APP =====================
if __name__ == "__main__":
    app.run(debug=True)
