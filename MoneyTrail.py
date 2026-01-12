income = []
expense = []
saving =[]
balance = 0
from datetime import datetime, timedelta

def print_table(headers, rows):
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build lines
    line = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_line = "|" + "|".join(f" {headers[i]:<{col_widths[i]}} " for i in range(len(headers))) + "|"

    print(line)
    print(header_line)
    print(line)

    for row in rows:
        print("|" + "|".join(f" {str(row[i]):<{col_widths[i]}} " for i in range(len(row))) + "|")

    print(line)



def addIncome():
    global balance
    print("\nADD MONEY")
    money = int(input("How much money Rp. "))
    if money <= 0:
        print("Invalid Amount")
        return
    else:
        history = datetime.now().strftime("%d/%m/%Y")
        income.append({"money": money, "history": history})
        balance += money
        print(f"Added Rp.{money} on {history}\n")
        return

def spendMoney():
    global balance
    print("\nSPEND MONEY")
    category = input("What category do you want spend on: ")
    spending = int(input("How much money Rp. "))
    if spending <= 0:
        print("Invalid Amount")
    elif spending > balance:
        print("Not enough balance")
    else:
        history = datetime.now().strftime("%d/%m/%Y")
        expense.append({"category": category, "spending": spending, "history": history})
        balance -= spending
        print(f"Spent Rp.{spending} on {history}")
        return

def saveMoney():
    global balance
    print("\nSAVE MONEY")
    if saving:
        print("Existing Saving:")
        for i, item in enumerate(saving, start=1):
            print(f"{i}. {item['name']} | Savings: {item['save']}")
    else:
        print("No savings Yet.")
    name = input("Type saving name (existing or new): ").strip()
    save = int(input("How much Rp. "))
    if save <= 0:
        print("Invalid Amount")
        return
    if save > balance:
        print("Not enough balance")
        return
    history = datetime.now().strftime("%d/%m/%Y")
    found = False
    for item in saving:
        if name == item["name"]:
            item["save"] += save
            item["history"] += f", {history}"
            found = True
            break
    if not found:
        saving.append({"name": name, "save": save, "history": history})
    balance -= save
    print(f"Saved Rp.{save} on {history}\n")
    return

def withdrawSaving():
    global balance
    if not saving:
        print("No savings available.")
        return
    print("\nWITHDRAW FROM SAVINGS")
    rows = []
    for i, item in enumerate(saving, start=1):
        rows.append([
            i,
            item["name"],
            f"Rp.{item['save']}"
        ])
    print_table(
        ["No", "Saving Name", "Amount Saved"],
        rows
    )
    choice = int(input("Choose saving number: "))
    if choice < 1 or choice > len(saving):
        print("Invalid choice.")
        return
    item = saving[choice - 1]
    amount = int(input("Withdraw amount Rp. "))
    if amount <= 0:
        print("Invalid amount.")
        return
    if amount > item["save"]:
        print("Not enough money in this saving.")
        return
    item["save"] -= amount
    balance += amount
    date = datetime.now().strftime("%d/%m/%Y")
    item["history"] += f", -{amount}({date})"
    print(f"Withdrawn Rp.{amount} from '{item['name']}' on {date}")


def showBalance():
    global balance
    while True:
        print("\nSHOW BALANCE")
        print("1. Show Balance Amount")
        print("2. Show Expenses")
        print("3. Show savings")
        print("4. Exit")
        choice = int(input("Choose: "))
        match choice:
            case 1:
                print(f"Current Balance: Rp.{balance},-")
            case 2:
                print("\nSHOW EXPENSES")
                print("1. Weekly (Last 7 Days)")
                print("2. Monthly")
                option = int(input("Choose: "))

                rows = []
                total = 0

                if option == 1:
                    today = datetime.now()
                    last_week = today - timedelta(days=7)

                    for item in expense:
                        d = datetime.strptime(item["history"], "%d/%m/%Y")
                        if last_week <= d <= today:
                            rows.append([
                                item["category"],
                                f"Rp.{item['spending']}",
                                item["history"]
                            ])
                            total += item["spending"]

                    print("\nWEEKLY EXPENSES")
                    if rows:
                        print_table(
                            ["Category", "Amount", "Date"],
                            rows
                        )
                        print(f"Total Weekly Spending: Rp.{total}")
                    else:
                        print("No expenses in the last 7 days.")

                elif option == 2:
                    month = int(input("Month (1-12): "))
                    year = int(input("Year: "))

                    for item in expense:
                        d = datetime.strptime(item["history"], "%d/%m/%Y")
                        if d.month == month and d.year == year:
                            rows.append([
                                item["category"],
                                f"Rp.{item['spending']}",
                                item["history"]
                            ])
                            total += item["spending"]

                    print(f"\nMONTHLY EXPENSES {month}/{year}")
                    if rows:
                        print_table(
                            ["Category", "Amount", "Date"],
                            rows
                        )
                        print(f"Total Monthly Spending: Rp.{total}")
                    else:
                        print("No expenses found for this month.")
            case 3:
                print("\nSAVINGS")

                if not saving:
                    print("No savings yet.")
                    return

                rows = []
                for item in saving:
                    rows.append([
                        item["name"],
                        f"Rp.{item['save']}",
                        item["history"]
                    ])

                print_table(
                    ["Saving Name", "Amount", "History"],
                    rows
                )
            case 4:
                break
            case _:
                print("Invalid Choice")            

def mainMenu():
    while True:
        print("\nWELCOME FARRAS")
        print("1. Add Income")
        print("2. Spend Something")
        print("3. Save your Money")
        print("4. Withdraw from Savings")
        print("5. Show Balance")
        print("6. Exit")
        
        choice = int(input("Choose: "))
        match choice:
            case 1:
                addIncome()
            case 2:
                spendMoney()
            case 3:
                saveMoney()
            case 4:
                withdrawSaving()
            case 5:
                showBalance()
            case 6:
                break
            case _:
                print("Invalid choice")

if __name__ == "__main__":
    mainMenu()