# ================ GLOBAL DATA ==================

library = []
users = {}
current_user = None

# ================ BOOK DISPLAY ==================

def showBook():
    if not library:
        print("No Book currently in stock")
        print()
        return
    book_width = max(len(item["Book"]) for item in library)
    book_width = max(book_width, len("Book Name"))
    qty_width = 10
    WIDTH = book_width + qty_width * 3 + 5
    print("=" * WIDTH)
    print("|" + "LIBRARY INVENTORY".center(WIDTH - 2) + "|")
    print("=" * WIDTH)
    print(f"|{'Book Name':<{book_width}}|{'Available':<{qty_width}}|{'Borrowed':<{qty_width}}|{'Max':<{qty_width}}|")
    print("-" * WIDTH)
    for item in library:
        print(f"|{item['Book']:<{book_width}}|{item['Quantity']:<{qty_width}}|{item['Borrowed']:<{qty_width}}|{item['MaxQuantity']:<{qty_width}}|")
    print("=" * WIDTH)
    print()

# ========================= ADMIN CONTROL ==============================
def addExistingbook():
    book = input("Book Name: ")
    for item in library:
        if book == item["Book"]:
            print(f"Total Book {item['Quantity']}, Cap at {item['MaxQuantity']}, borrowed: {item['Borrowed']}")
            add  = int(input("How many books do you want to add: "))
            if add < 0:
                print("Cannot Input under 0")
                return
            else:
                item["MaxQuantity"] += add
                item["Quantity"] += add
                print("Stock Updated")
                print()
                return
    print("Book not Found!")

def addBooks():
    book = input("Name of the book: ")
    for item in library:
        if item["Book"] == book:
            print("This book already exist")
            print()
            return
    Qty = int(input("How many books: "))
    library.append({"Book": book, "Quantity": Qty, "MaxQuantity": Qty, "Borrowed": 0})
    print("Book Added Succesfully")
    print()
    return

def removeBook():
    book = input("Book Name: ")
    for item in library:
        if book == item["Book"]:
            library.remove(item)
            print("Book has been removed")
            print()
            return
    print("Book Not found")

def adminLogin():
    username = "admin"
    password = 1234
    print("Admin Login")
    usernameLogin = input("Username: ")
    passwordLogin = int(input("Password: "))
    if usernameLogin == username and passwordLogin == password:
        adminMenu()
    else:
        print("Incorrect username or password")

def adminMenu():
    while True:
        print("\nADMIN MENU")
        print("1. Add New book")
        print("2. Add Existing Book")
        print("3. Remove book")
        print("4. Show books")
        print("5. Logout")

        choice = int(input("Choose: "))
        match choice:
            case 1:
                addBooks()
            case 2:
                addExistingbook()
            case 3:
                removeBook()
            case 4:
                showBook()
            case 5:
                return
            case _:
                print("Invalid Choice")

# ========================= USER FUNCTIONS ==============================

def borrowBook():
    global current_user
    book = input("Book Name: ")
    for item in library:
        if book == item["Book"]:
            print(f"Total book of {book} quantity: {item['Quantity']}")
            while True:
                borrow = int(input("How many Books you want to borrow: "))
                if borrow > item["Quantity"]:
                    print("Borrowing Exceed the total of books")
                elif borrow <= 0:
                    print("Cannot below or equal to 0")
                else:
                    item["Quantity"] -= borrow
                    item["Borrowed"] += borrow
                    user_books = users[current_user]["Borrowed"]
                    user_books[book] = user_books.get(book, 0) + borrow
                    print("Thank you for Borrowing")
                    print()
                    return
    print("Book not Found!")

def returnBook():
    user_books = users[current_user]["Borrowed"]
    if not user_books:
        print("You have no borrowed books\n")
        return
    book = input("Name of the Book: ")
    if book not in user_books:
        print("You did not borrow this book\n")
        return
    returning = int(input("How many books do you want to return: "))
    if returning <= 0 or returning > user_books[book]:
        print("Invalid amount\n")
        return
    for item in library:
        if item["Book"] == book:
            item["Quantity"] += returning
            item["Borrowed"] -= returning
            break
    user_books[book] -= returning
    if user_books[book] == 0:
        del user_books[book]
    print("Thank you for returning the book(s)\n")

def searchBook():
    keyword = input("Search Book: ").upper()
    found = False
    for item in library:
        title = item["Book"].upper()
        clean_title = title.replace(":", "").replace("'", "").replace(",", "").replace(".", "").replace("-", "").replace("_", "")
        word = clean_title
        if keyword in word:
            print(f"{item['Book']} (Available: {item['Quantity']})")
            found = True
    if not found:
        print("Book not Found!")
    print()

def userMenu():
    while True:
        print("\nUSER ACCESS")
        print("1. Register")
        print("2. Login")
        print("3. Back")

        choice = int(input("Choose: "))
        match choice:
            case 1:
                userRegister()
            case 2:
                userLogin()
            case 3:
                return
            case _:
                print("Invalid Choice")

def userRegister():
    username = input("Username: ").lower()
    if username in users:
        print("Username already exists\n")
        return
    users[username] = {"Borrowed": {}}
    print("User registered succesfully\n")


def userLogin():
    global current_user
    username = input("Username: ")
    if username not in users:
        print("User not Found!")
        print()
        return
    else:
        current_user = username
        print(f"Welcome {username}!\n")
        userDashboard()

def userDashboard():
    while True:
        print("\nUSER MENU")
        print("1. Borrow book")
        print("2. Return book")
        print("3. My borrowed books")
        print("4. Search for a Book")
        print("5. Logout")

        choice = int(input("Choose: "))
        match choice:
            case 1:
                borrowBook()
            case 2:
                returnBook()
            case 3:
                showMyBook()
            case 4:
                searchBook()
            case 5:
                return
            case _:
                print("Invalid Choice")

def showMyBook():
    borrowed = users[current_user]["Borrowed"]
    if not borrowed:
        print("You haven't borrowed any books yet.\n")
        return
    print("My Borrowed Books")
    print("-----------------")
    for book, qty in borrowed.items():
        print(f"{book} (Borrowed: {qty})")

# ================ MAIN MENU ==================
def mainMenu():
    while True:
        print("\n1. Admin")
        print("2. User")
        print("3. Exit")

        choice = int(input("Choose: "))
        match choice:
            case 1:
                adminLogin()
            case 2:
                userMenu()
            case 3:
                break
            case _:
                print("Invalid Choice")

# ================ PROGRAM ENTRY ==================
if __name__ == "__main__":
    mainMenu()