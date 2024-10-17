import sqlite3


def conn_db():
    conn = sqlite3.connect("budget.sqlite")
    cursor = conn.cursor()
    return conn, cursor  # return both conn and cursor (not sure why - check this)


def close_db(conn):
    conn.commit()
    conn.close()


def create_table():
    conn, cursor = conn_db()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL
    )
    """
    )  # CREATE TABLE IF NOT EXISTS -- edit to this, if I am getting an error
    close_db(conn)


# # ###############################################################################


def enter_transaction(type):
    amount = float(input(f"Enter {type} amount: "))
    category = input(f"Enter {type} category: ")
    conn, cursor = conn_db()
    cursor.execute(
        "INSERT INTO Finances (type, amount, category) VALUES (?, ?, ?)",
        (type, amount, category),
    )
    close_db(conn)
    print(f"{type.capitalize()} added successfully!")


def get_balance():
    conn, cursor = conn_db()
    cursor.execute(
        "SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) FROM Finances"
    )
    balance = cursor.fetchone()[0] or 0
    close_db(conn)
    print(f"Current balance: {balance:.2f}")


def get_all_transactions(type):
    conn, cursor = conn_db()
    cursor.execute("SELECT * FROM Finances WHERE type=?", (type,))
    transactions = cursor.fetchall()
    close_db(conn)
    print(f"All {type}s:")
    for transaction in transactions:
        print(
            f"ID: {transaction[0]}, Type: {transaction[1]}, Amount: {transaction[2]}, Category: {transaction[3]}"
        )


def delete_transaction():
    id = int(input("Enter the ID of the transaction to delete: "))
    conn, cursor = conn_db()
    cursor.execute("DELETE FROM Finances WHERE id=?", (id,))
    close_db(conn)
    print("Transaction deleted successfully!")


def update_transaction():
    id = int(input("Enter the ID of the transaction to update: "))
    type = input("Enter new type (income/expense): ")
    amount = float(input("Enter new amount: "))
    category = input("Enter new category: ")
    conn, cursor = conn_db()
    cursor.execute(
        "UPDATE Finances SET type=?, amount=?, category=? WHERE id=?",
        (type, amount, category, id),
    )
    close_db(conn)
    print("Transaction updated successfully!")


def main_menu():
    while True:
        print("\n--- BUDGET APP ---")
        print("1. Enter income")
        print("2. Enter expense")
        print("3. Get balance")
        print("4. Get all incomes")
        print("5. Get all expenses")
        print("6. Delete transaction")
        print("7. Update transaction")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            enter_transaction("income")
        elif choice == "2":
            enter_transaction("expense")
        elif choice == "3":
            get_balance()
        elif choice == "4":
            get_all_transactions("income")
        elif choice == "5":
            get_all_transactions("expense")
        elif choice == "6":
            delete_transaction()
        elif choice == "7":
            update_transaction()
        elif choice == "8":
            print("Thank you for using Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_table()
    main_menu()
