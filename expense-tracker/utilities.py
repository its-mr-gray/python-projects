"""
utilities.py

contains all functionality for the CLI
"""

import csv
import sqlite3
from datetime import datetime


def init_db(db: str = "expenses.db") -> None:
    """
    Implicitly creates a sqlite db if it doesn't exist, then creates an expenses table if it doesn't exist.

    Args:
        db (str): The path to the database.

    Returns:
        None
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        description TEXT,
        amount REAL, 
        category TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_expense(
    description: str, amount: float, category: str, db="expenses.db"
) -> None:
    """
    Adds a new entry to the expenses table.

    Args:
        description (str): A description of the expense.
        amount (float): The total amount of the expense.
        category (str): The category of the expense.
        db (str): The path to the database.

    Returns:
        None
    """
    date = datetime.today().isoformat()

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses (date,description,amount,category) VALUES (?,?,?,?)",
        (date, description, amount, category),
    )

    conn.commit()
    conn.close()

    view_total_expenses(db)


def view_total_expenses(db="expenses.db") -> str:
    """
    Lists all expenses.

    Args:
        db (str): The path to the database.

    Returns:
        str: A formatted string representing the expenses table for terminal output.
    """

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM expenses
    """)

    conn.commit()
    result = cur.fetchall()
    conn.close()

    if len(result) > 0:
        header, rows = format_output(result=result)

        return f"{header}\n{rows}"
    else:
        return "Empty expense table. Run the 'add' command to add expenses."


def summarize_all_expenses(db="expenses.db"):
    """
    Aggregates all expenses.

    Args:
        db (str): The path to the database.

    Returns:
        None
    """

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(amount)
        FROM expenses 
    """)

    result = cur.fetchone()
    conn.close()

    total = result[0]

    print(total)


def summarize_category_expenses(category, db="expenses.db"):
    """
    Aggregates expenses by category.

    Args:
        category (str): The category of expense.
        db (str): The path to the database.

    Returns:
        None
    """
    current_categories = get_current_categories(db)
    if category not in current_categories:
        print(
            f"{category} does not exist. Run the view command to see all current expenses/categories."
        )
    else:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(
            """
            SELECT 
            SUM(amount)
            FROM expenses
            WHERE
            category = ?
            """,
            (category,),
        )

        conn.commit()
        result = cur.fetchone()
        conn.close()

        amount = result[0]
        print(amount)


def summarize_monthly_expenses(month: int, db="expenses.db"):
    """
    Aggregates expenses by category.

    Args:
        month (int): The integer value of the expense month (i.e., August = 8)
        db (str): The path to the database.

    Returns:
        None
    """
    formatted_month = f"{month:02d}"
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
        SUM(amount)
        FROM expenses
        WHERE
        strftime('%m', date) = ?
        """,
        (formatted_month,),
    )

    conn.commit()
    result = cur.fetchone()
    conn.close()

    amount = result[0]
    if amount:
        print(amount)
    else:
        dt = datetime(year=datetime.now().year, month=int(formatted_month), day=1)
        print(
            f"No expenses for the month of {dt.strftime('%B')}. Run the view command to see a list of all current dates of expenses."
        )


# TODO handle invalid ids
def remove_expense(id, db="expenses.db"):
    """
    Removes an expense.

    Args:
        id (int): The ID of the expense to be removed.
        db (str): The path to the datebase

    Returns:
        None
    """
    try:
        int(id)
    except ValueError:
        print(f"Error: ID {id} is not a valid integer.")

        return

    current_ids = get_current_ids(db)

    if int(id) not in current_ids:
        print(
            f"Error: ID #{id} is not valid. Run the 'view' command to see current IDs"
        )
    else:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (id,),
        )
        conn.commit()
        conn.close()

        view_total_expenses(db)


def format_output(result: list) -> (str, str):
    """
    Formats output for pretty printing to terminal.

    Args:
        result (list): A list of fetched query items

    Returns:
        tuple[str,str]: A tuple containing the formatted table headers and table rows as strings.
    """
    header = (
        f"{'ID':<4} {'Date':<12} {'Description':<20} {'Amount':<8} {'Category':<12}"
    )
    for item in result:
        id, date, desc, amount, cat = item
        date = datetime.fromisoformat(date)
        date = date.strftime("%Y-%m-%d")
        rows = f"{id:<4} {date:<12} {desc:<20} ${amount:<8.2f} {cat:<12}"

    return header, rows


# TODO validation, error handling
def export_to_csv(db="expenses.db", csv_path="expenses.csv"):
    """
    Exports all expenses to a csv file.

    Args:
        db (str): The path to the database.
        csv_path (str): The path to the csv file.

    Returns:
        None
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SElECT * FROM expenses
    """)
    rows = cur.fetchall()
    headers = [header[0] for header in cur.description]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(headers)
        writer.writerow(rows)

    conn.close()

    print(f"Expenses successfully exported! Path: {csv_path}")


def get_current_ids(db="expenses.db") -> list:
    """
    Helper function for retrieving existing IDs in the expense table. Used for error validation.

    Args:
        db (str): The path to the database.

    Returns:
        list[int]: A list of all current IDs within the table.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT id
        FROM expenses
    """)
    result = [item[0] for item in cur.fetchall()]
    conn.close()

    return result


def get_current_categories(db="expenses.db"):
    """
    Helper function for retrieving existing categories in the expense table. Used for error validation.

    Args:
        db (str): The path to the database.

    Returns:
        list[str]: A list of all current categories within the table
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT category
        FROM expenses
    """)
    result = [item[0] for item in cur.fetchall()]
    conn.close()

    return result
