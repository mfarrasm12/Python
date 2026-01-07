library = []

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

def addExistingbook():
    book = input("Book Name: ")
    for item in library:
        if book == item["Book"]:
            print(f"Total Book {item['Quantity']}, Cap at {item['MaxQuantity']}, borrowed: {item['Borrowed']}")
            while True:
                add  = int(input("How many books do you want to add: "))
                if add < 0:
                    print("Cannot Input under 0")
                else:
                    item["MaxQuantity"] += add
                    item["Quantity"] += add
                    print("Thank you")
                    print()
                    return
    print("Book not Found!")

def addBooks():
    while True:
        book = input("Name of the book: ")
        for item in library:
            if item["Book"] == book:
                print("This book already exist")
                print()
                return
        Qty = int(input("How many books: "))
        library.append({"Book": book, "Quantity": Qty, "MaxQuantity": Qty, "Borrowed": 0})
        print("Added Succesfully")
        print()
        return

def borrowBook():
    while True:
        book = input("Book Name: ")
        for item in library:
            if book == item["Book"]:
                print(f"Total book of {book} quantity: {item['Quantity']}")
                while True:
                    borrow = int(input("How many Books you want to borrow: "))
                    if borrow > item["Quantity"]:
                        print("Borrowing Exceed the total of books")
                    elif borrow < 0:
                        print("Cannot below 0")
                    else:
                        item["Quantity"] -= borrow
                        item["Borrowed"] += borrow
                        print("Thank you for Borrowing")
                        print()
                        return
        print("Book not Found!")

def returnBook():
    book = input("Name of the Book: ")
    for item in library:
        if book == item["Book"]:
            while True:
                available_space = item["MaxQuantity"] - item["Quantity"]
                returning = int(input("How Many Books Do You Want To Return: "))
                if returning > available_space:
                    print(f"Quantity capped at {item['MaxQuantity']}")
                elif returning < 0:
                    print("Cannot Input Below 0")
                else:
                    item["Quantity"] += returning
                    item["Borrowed"] -= returning
                    print("Thank you for returning")
                    return
                print()
    print("Book Not found!")

def removeBook():
    book = input("Book Name: ")
    for item in library:
        if book == item["Book"]:
            library.remove(item)
            print("Book has been removed")
            print()
            return
    print("Book Not found")

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

                            
while True:
    print("1. ADD BOOKS")
    print("2. BORROW BOOKS")
    print("3. RETURN BOOKS")
    print("4. ADD EXISTING BOOK")
    print("5. SEARCH FOR A BOOK")
    print("6. SHOW AVAILABLE BOOKS")
    print("7. REMOVE BOOK")
    print("8. EXIT")

    choice = int(input("Choose: "))
    match choice:
        case 1:
            addBooks()
        case 2:
            borrowBook()
        case 3:
            returnBook()
        case 4:
            addExistingbook()
        case 5:
            searchBook()
        case 6:
            showBook()
        case 7:
            removeBook()
        case 8:
            print("Thank You for Visiting")
            break
        case _:
            print("Choice Not Valid")