library = []

def showBook():
    for item in library:
        print(item)
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
                            
while True:
    print("1. ADD BOOKS")
    print("2. BORROW BOOKS")
    print("3. RETURN BOOKS")
    print("4. ADD EXISTING BOOK")
    print("5. SHOW AVAILABLE BOOKS")
    print("6. REMOVE BOOK")
    print("7. EXIT")

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
            showBook()
        case 6:
            removeBook()
        case 7:
            print("Thank You for Visiting")
            break
        case _:
            print("Choice Not Valid")