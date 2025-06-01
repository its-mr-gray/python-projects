"""
utilities.py

contains all functionality for the CLI
"""

import csv
import sqlite3
from argparse import Namespace
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


def add_expense(description: str, amount: float, category: str, db="expenses.db"):
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
    init_db(db)

    date = datetime.today().isoformat()

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses (date,description,amount,category) VALUES (?,?,?,?)",
        (date, description, amount, category),
    )

    conn.commit()
    conn.close()

    print(f"Expense successfully added! Current expenses:\n {view_total_expenses(db)}")


def view_total_expenses(db="expenses.db") -> str:
    """
    Lists all expenses.

    Args:
        db (str): The path to the database.

    Returns:
        str: A formatted string representing the expenses table for terminal output.
    """
    init_db(db)

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


def summarize_all_expenses(db="expenses.db") -> float:
    """
    Aggregates all expenses.

    Args:
        db (str): The path to the database.

    Returns:
        float: The total amount of all expenses in the database.
    """
    init_db(db)

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(amount)
        FROM expenses 
    """)

    result = cur.fetchone()
    conn.close()

    total = result[0]

    return total


def summarize_category_expenses(category, db="expenses.db") -> str:
    """
    Aggregates expenses by category.

    Args:
        category (str): The category of expense.
        db (str): The path to the database.

    Returns:
        str: A string containing the total amout of expenses for the given category.
    """
    init_db(db)

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
        return f"Total expenses for {category}: {amount}"


def summarize_monthly_expenses(month: int, db="expenses.db") -> None | str:
    """
    Aggregates expenses by a given integer month.

    Args:
        month (int): The integer value of the expense month (i.e., August = 8)
        db (str): The path to the database.

    Returns:
        None
        str: A message regarding the success/failure of the monthly expense check.
    """
    init_db(db)

    try:
        int(month)
    except ValueError:
        print(f"{month} is not valid. Month must be an int (i.e, 5 for 'May')")

        return

    formatted_month = f"{month:02d}"
    dt = datetime(year=datetime.now().year, month=int(formatted_month), day=1)
    month_in_text = dt.strftime("%B")
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

    result = cur.fetchone()
    conn.close()

    amount = result[0]

    if not amount:
        return f"No expenses for the month of {month_in_text}. Run the view command to see a list of all current dates of expenses."
    else:
        return f"Total expenses for {month_in_text}: {amount}"


def summarize_category_monthly_expenses(
    category: str, month: int, db="expenses.db"
) -> str:
    """
    Summarizes expenses by category within a given month.

    Args:
        category (str): The category to aggregate by.
        month (int): The integer month to filter by.

    Returns:
        str: A message containing the total amount of expenses within the filter criteria.
    """
    init_db(db)

    try:
        int(month)
    except ValueError:
        print(f"{month} is not valid. Month must be an int (i.e, 5 for 'May')")

        return

    current_categories = get_current_categories(db)
    formatted_month = f"{month:02d}"
    dt = datetime(year=datetime.now().year, month=int(formatted_month), day=1)
    month_in_text = dt.strftime("%B")

    if category not in current_categories:
        print(
            f"{category} does not exist. Run the view command to see all current expenses/categories."
        )

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
        SUM(amount)
        FROM expenses
        WHERE
        [strftime('%m', date) = ?]
        AND
        [category = ?]
        """,
        (formatted_month, category),
    )

    result = cur.fetchone()
    conn.close()

    amount = result[0]

    if not amount:
        return f"No {category} expenses for the month of {month_in_text}. Run the view command to see a list of all current dates of expenses."
    else:
        return f"Total {category} expenses for {month_in_text}: {amount}"


def update_expense_description(id: int, description: str, db="expenses.db") -> str:
    """
    Updates description of expense at given ID.

    Args:
        id (int): ID of expense to be updated.
        description (str): Updated description.
        db (str): The path to the database.

    Returns:
        str: A message indicating update success and showing current expenses table.
    """
    init_db(db)

    try:
        int(id)
    except ValueError:
        print(
            "Error: ID must be an integer. Run the 'view' command to see existing expense IDs."
        )

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE expenses
        SET description = ?
        WHERE id = ?
        """,
        (
            description,
            id,
        ),
    )
    conn.commit()
    conn.close()

    return f"Description updated for expense!\n{view_total_expenses(db)}"


def update_expense_amount(id: int, amount: float, db="expenses.db") -> str:
    """
    Updates amount of expense at given ID.

    Args:
        id (int): ID of expense to be updated.
        amount (float): Updated amount.
        db (str): The path to the database.

    Returns:
        str: A message indicating update success and showing current expenses table.
    """
    init_db(db)

    try:
        int(id)
    except ValueError:
        print(
            "Error: ID must be an integer. Run the 'view' command to see existing expense IDs."
        )

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE expenses
        SET amount = ?
        WHERE id = ?
        """,
        (
            amount,
            id,
        ),
    )
    conn.commit()
    conn.close()

    return f"Amount updated for expense!\n{view_total_expenses(db)}"


def update_expense_category(id: int, category: str, db="expenses.db") -> str:
    """
    Updates category of expense at given ID.

    Args:
        id (int): ID of expense to be updated.
        category (str): Updated category.
        db (str): The path to the database.

    Returns:
        str: A message indicating update success and showing current expenses table.
    """
    init_db(db)

    try:
        int(id)
    except ValueError:
        print(
            "Error: ID must be an integer. Run the 'view' command to see existing expense IDs."
        )

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE expenses
        SET category = ?
        WHERE id = ?
        """,
        (
            category,
            id,
        ),
    )
    conn.commit()
    conn.close()

    return f"Category updated for expense!\n{view_total_expenses(db)}"


def remove_expense(id, db="expenses.db") -> None | str:
    """
    Removes an expense.

    Args:
        id (int): The ID of the expense to be removed.
        db (str): The path to the datebase

    Returns:
        None
        str: A success message indicating removal expense at given ID. Also prints current table of expenses.
    """
    init_db(db)

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

    print(
        f"Expense at {id} removed! Current expenses tracked:\n {view_total_expenses(db)}"
    )


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
    lines = []
    for item in result:
        id, date, desc, amount, cat = item
        date = datetime.fromisoformat(date)
        date = date.strftime("%Y-%m-%d")
        lines.append(f"{id:<4} {date:<12} {desc:<20} ${amount:<8.2f} {cat:<12}")
    rows = "\n".join(lines)
    return header, rows


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


def handle_add(args: Namespace) -> None:
    """
    Handles the CLI arguments for adding expenses in the database.

    Parameters:
        args (Namespace): Parsed command line fields containing fields for expense creation.

    Side-Effects:
        Adds a new expense to the database.

    Returns:
        None
    """
    add_expense(args.description, args.amount, args.category)


def handle_view(args: Namespace) -> None:
    """
    Handles the CLI arguments for viewing expenses.

    Parameters:
        args (Namespace): Parse command for expense viewing.

    Returns:
        None
    """
    print(view_total_expenses())


def handle_summary(args: Namespace) -> None:
    """
    Handles the CLI arguments for summarizing expenses in the database.

    Parameters:
        args (Namespace): Parsed command line fields containing filtration options for summarization.

    Returns:
        None
    """
    match (args.category, args.monthly):
        case (str() as cat, int() as month):
            print(summarize_category_monthly_expenses(cat, month))
        case (None, int() as month):
            print(summarize_monthly_expenses(month))
        case (str() as cat, None):
            print(summarize_category_expenses(cat))
        case (None, None):
            print(summarize_all_expenses())


def handle_update(args: Namespace) -> None:
    """
    Handles the CLI arguments for updating expenses in the database.

    Parameters:
        args (Namespace): Parsed command line fields containing integer ID and fields for updating.

    Side-Effects:
        Updates given fields at the given ID in the databased and prints updated table to the terminal.

    Returns:
        None
    """
    match (args.id, args.description, args.amount, args.category):
        case (int() as id, str() as desc, float() as amount, str() as cat):
            print(
                update_expense_description(id, desc),
                update_expense_amount(id, amount),
                update_expense_category(id, cat),
            )
        case (int() as id, None, float() as amount, str() as cat):
            print(update_expense_amount(id, amount), update_expense_category(id, cat))
        case (int() as id, str() as desc, None, str() as cat):
            print(
                update_expense_description(id, desc), update_expense_category(id, cat)
            )
        case (int() as id, str() as desc, float() as amount, None):
            print(
                update_expense_description(id, desc), update_expense_amount(id, amount)
            )
        case (int() as id, None, None, None):
            print("Nothing to update.")


def handle_remove(args: Namespace) -> None:
    """
    Handles the CLI arguments for removing expenses in the database.

    Parameters:
        args (Namespace): Parsed command line fields containing integer ID for expense to be removed.

    Side-Effects:
        Removes expense from database.

    Returns:
        None
    """
    remove_expense(args.id)


def handle_export(args: Namespace) -> None:
    """
    Handles the CLI arguments for exporting expenses to a csv.

    Parameters:
        args (Namespace): Parsed command line fields for export.

    Side-Effects:
        Exports the expense table to a .csv file.

    Returns:
        None
    """
    export_to_csv()
