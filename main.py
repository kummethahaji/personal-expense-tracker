import sqlite3


def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT UNIQUE NOT NULL,
            budget_amount REAL NOT NULL
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


def view_category_summary(cursor):
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    summary = cursor.fetchall()

    if not summary:
        print("No expenses found.")
        return

    print("\n--- Category-Wise Spending Summary ---")
    for category, total in summary:
        print(f"{category}: ₹{total:.2f}")


def view_monthly_summary(cursor):
    month = input("Enter month (YYYY-MM): ").strip()

    if len(month) != 7 or month[4] != "-":
        print("Invalid format. Please use YYYY-MM.")
        return

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (month,))

    total = cursor.fetchone()[0] or 0
    print(f"\nTotal spending for {month}: ₹{total:.2f}")


def set_monthly_budget(cursor, connection):
    month = input("Enter month (YYYY-MM): ").strip()

    if len(month) != 7 or month[4] != "-":
        print("Invalid format. Please use YYYY-MM.")
        return

    try:
        budget_amount = float(input("Enter monthly budget amount: ₹"))
    except ValueError:
        print("Invalid budget amount. Please enter a number.")
        return

    if budget_amount <= 0:
        print("Budget amount must be greater than zero.")
        return

    cursor.execute("""
        INSERT INTO budgets (month, budget_amount)
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET budget_amount = excluded.budget_amount
    """, (month, budget_amount))

    connection.commit()
    print(f"Budget for {month} saved successfully!")


def view_budget_status(cursor):
    month = input("Enter month (YYYY-MM): ").strip()

    if len(month) != 7 or month[4] != "-":
        print("Invalid format. Please use YYYY-MM.")
        return

    cursor.execute(
        "SELECT budget_amount FROM budgets WHERE month = ?",
        (month,)
    )
    budget = cursor.fetchone()

    if not budget:
        print(f"No budget has been set for {month}.")
        return

    budget_amount = budget[0]

    cursor.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE substr(expense_date, 1, 7) = ?
    """, (month,))
    spent = cursor.fetchone()[0] or 0

    remaining = budget_amount - spent

    print(f"\n--- Budget Status for {month} ---")
    print(f"Budget: ₹{budget_amount:.2f}")
    print(f"Spent: ₹{spent:.2f}")

    if remaining >= 0:
        print(f"Remaining: ₹{remaining:.2f}")
        print("Status: You are within your budget.")
    else:
        print(f"Overspent by: ₹{abs(remaining):.2f}")
        print("Status: Warning! You have exceeded your budget.")


def edit_expense(cursor, connection):
    try:
        expense_id = int(input("Enter the expense ID to edit: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()

    if not expense:
        print("Expense ID not found.")
        return

    print(f"\nEditing: ₹{expense[1]:.2f} | {expense[2]} | {expense[3]} | {expense[4]}")

    try:
        amount = float(input("Enter new amount: ₹"))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Enter new category: ").strip()
    expense_date = input("Enter new date (YYYY-MM-DD): ").strip()
    note = input("Enter new note: ").strip()

    if not category or not expense_date:
        print("Category and date cannot be empty.")
        return

    cursor.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, expense_date = ?, note = ?
        WHERE id = ?
    """, (amount, category, expense_date, note, expense_id))

    connection.commit()
    print("Expense updated successfully!")


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

    create_tables(cursor)
    connection.commit()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Category-Wise Summary")
        print("5. Monthly Spending Summary")
        print("6. Set or Update Monthly Budget")
        print("7. View Budget Status")
        print("8. Edit Expense")
        print("9. Delete Expense")
        print("10. Exit")

        choice = input("Choose an option (1-10): ").strip()

        if choice == "1":
            add_expense(cursor, connection)
        elif choice == "2":
            view_expenses(cursor)
        elif choice == "3":
            view_total(cursor)
        elif choice == "4":
            view_category_summary(cursor)
        elif choice == "5":
            view_monthly_summary(cursor)
        elif choice == "6":
            set_monthly_budget(cursor, connection)
        elif choice == "7":
            view_budget_status(cursor)
        elif choice == "8":
            edit_expense(cursor, connection)
        elif choice == "9":
            delete_expense(cursor, connection)
        elif choice == "10":
            connection.close()
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1 to 10.")


if __name__ == "__main__":
    main()