"""
utilities.py

contains all functionality for the CLI
"""

import datetime
import sqlite3


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
    """
    date = datetime.datetime.today().isoformat()

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO expenses (date,description,amount,category) VALUES (?,?,?,?)"(
            date, description, amount, category
        )
    )

    conn.commit()
    conn.close()
