library = []

def showBook():
    for item in library:
        print(item)

def addBooks():
    book = input("Name of the book: ")
    Qty = int(input("How many books: "))
    library.append({"Book": book, "Quantity": Qty, "MaxQuantity": Qty})
    print("Added Succesfully")

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
                    else:
                        item["Quantity"] -= borrow
                        print("Thank you for Borrowing")
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
                else:
                    item["Quantity"] += returning
                    print("Thank you for returning")
                    return
    print("Book Not found!")
                            
while True:
    print("1. ADD BOOKS")
    print("2. BORROW BOOKS")
    print("3. RETURN BOOK")
    print("4. SHOW AVAILABLE BOOKS")
    print("5. EXIT")

    choice = int(input("Choose: "))
    match choice:
        case 1:
            addBooks()
        case 2:
            borrowBook()
        case 3:
            returnBook()
        case 4:
            showBook()
        case 5:
            print("Thank You for Visiting")
            break
        case _:
            print("Not a Valid Choice")