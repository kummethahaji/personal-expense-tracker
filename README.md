# Personal Expense Tracker

A command-line application built with Python and SQLite to help users manage daily expenses, track monthly budgets, and analyze spending patterns.

## Features

- Add new expenses
- View all saved expenses
- Edit an expense by ID
- Delete an expense by ID
- Calculate total spending
- View category-wise spending summary
- View monthly spending summary
- Set or update a monthly budget
- Check budget status and receive overspending alerts
- Store data securely using SQLite

## Technologies Used

- Python
- SQLite
- Git and GitHub

## Requirements

- Python 3.11 or later

No additional packages are required because `sqlite3` is included with Python.

## How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/kummethahaji/personal-expense-tracker.git
   ```

2. Open the project folder:

   ```bash
   cd personal-expense-tracker
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Menu Options

```text
1. Add Expense
2. View All Expenses
3. View Total Spending
4. Category-Wise Summary
5. Monthly Spending Summary
6. Set or Update Monthly Budget
7. View Budget Status
8. Edit Expense
9. Delete Expense
10. Exit
```

## Example Budget Status

```text
--- Budget Status for 2026-08 ---
Budget: ₹1000.00
Spent: ₹550.00
Remaining: ₹450.00
Status: You are within your budget.
```

## Database

The application automatically creates an SQLite database file named `expenses.db`.

It contains:

- `expenses` table — stores expense amount, category, date, and note
- `budgets` table — stores monthly budget amounts

## Future Improvements

- Add date validation
- Search expenses by category or date
- Export reports to CSV
- Build a graphical user interface using Tkinter
- Create a web version using Flask
- Add user login and authentication

## Author

Shaik Saheb  
GitHub: [kummethahaji](https://github.com/kummethahaji)
