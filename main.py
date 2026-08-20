import sqlite3


def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            note TEXT
        )
    """)


def add_expense(cursor, connection):
    try:
        amount = float(input("Enter expense amount: ₹"))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Enter category: ").strip()
    expense_date = input("Enter date (YYYY-MM-DD): ").strip()
    note = input("Enter a short note: ").strip()

    if not category or not expense_date:
        print("Category and date cannot be empty.")
        return

    cursor.execute("""
        INSERT INTO expenses (amount, category, expense_date, note)
        VALUES (?, ?, ?, ?)
    """, (amount, category, expense_date, note))

    connection.commit()
    print("Expense added successfully!")


def view_expenses(cursor):
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found.")
        return

    print("\n--- All Expenses ---")
    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: ₹{expense[1]:.2f} | "
            f"Category: {expense[2]} | "
            f"Date: {expense[3]} | "
            f"Note: {expense[4]}"
        )


def view_total(cursor):
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"\nTotal spending: ₹{total:.2f}")


def delete_expense(cursor, connection):
    try:
        expense_id = int(input("Enter the expense ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))

    if not cursor.fetchone():
        print("Expense ID not found.")
        return

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    connection.commit()
    print("Expense deleted successfully!")


def main():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    create_table(cursor)
    connection.commit()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense(cursor, connection)
        elif choice == "2":
            view_expenses(cursor)
        elif choice == "3":
            view_total(cursor)
        elif choice == "4":
            delete_expense(cursor, connection)
        elif choice == "5":
            connection.close()
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    main()