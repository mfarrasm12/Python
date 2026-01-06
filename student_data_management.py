data = []
def add_data():
    studentName = input("Name: ")
    NIM = int(input("NIM: "))
    score = int(input("score: "))

    data.append({
        "studentName": studentName,
        "NIM": NIM,
        "score": score
    })
    print("added succesfully")

def editData():
    while True:
        studentName = input("Enter name to edit: ")
        for item in data:
            if item["studentName"] == studentName:
                item["studentName"] = input("Enter new name: ")
                item["NIM"] = int(input("Enter new NIM: "))
                item["score"] = int(input("Enter new score:"))
                print("Data has been updated")
                return
        print("Name not found!")

def deleteData():
    while True:
        studentName = input("Enter name to delete: ")
        for item in data:
            if item["studentName"] == studentName:
                data.remove(item)
                print("Data has been deleted")
                return
        print("Name not found!")

def showData():
    for item in data:
        print(item)

def calculateData():
    scoreMax = data[0]["score"]
    scoreMin = data[0]["score"]
    total = 0

    for item in data:
        score = item["score"]
        if score > scoreMax:
            scoreMax = score
        if score < scoreMin:
            scoreMin = score
        total += score
    average = total /len(data)
    print(f"Maximum Score: {scoreMax}")
    print(f"minimum Score: {scoreMin}")
    print(f"Average Score: {average:.2f}")


while True:
    print("1. ADD STUDENT")
    print("2. SHOW DATA")
    print("3. EDIT DATA")
    print("4. DELETE DATA")
    print("5. CALCULATE DATA")
    print("6. EXIT")

    choice = int(input("Choose: "))
    match choice:
        case 1:
            add_data()
        case 2:
            showData()
        case 3:
            editData()
        case 4:
            deleteData()
        case 5:
            calculateData()
        case 6:
            print("Thank you")
            break
        case _:
            print("Invalid Choice")
