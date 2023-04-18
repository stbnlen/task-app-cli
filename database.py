import sqlite3
from typing import List
from model import Todo
import datetime

DATABASE_FILENAME = 'todos.db'
conn = sqlite3.connect(DATABASE_FILENAME)
c = conn.cursor()


def create_table():
    """
    Creates the 'todos' table in the SQLite database if it does not exist already.
    """
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
        )""", ())


create_table()


def insert_todo(todo: Todo):
    """
    Inserts a Todo object into the 'todos' table in the SQLite database.

    Args:
        todo (Todo): The Todo object to insert.

    Returns:
        None
    """
    try:
        c.execute('select count(*) FROM todos')
        count = c.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (?, ?, ?, ?, ?, ?)',
        (todo.task, todo.category, todo.date_added, todo.date_completed, todo.status, todo.position))


def get_all_todos() -> List[Todo]:
    """
    Retrieves all Todo objects from the 'todos' table in the SQLite database.

    Returns:
        List[Todo]: A list of all Todo objects in the table.
    """
    try:
        c.execute('select * from todos')
        results = c.fetchall()
    except sqlite3.Error as e:
        print('Database error:', e)
    return [Todo(*result) for result in results]



def delete_todo(position):
    """
    Deletes a Todo object from the 'todos' table in the SQLite database at the specified position.

    Args:
        position (int): The position of the Todo object to delete.

    Returns:
        None
    """
    c.execute('SELECT COUNT(*) FROM todos')
    count = c.fetchone()[0]
    if position < 1 or position > count:
        raise ValueError("Invalid position")
    try:
        with conn:
            c.execute("DELETE FROM todos WHERE position=:position", {"position": position})
            c.execute("UPDATE todos SET position = position - 1 WHERE position > :position", {"position": position})
    except sqlite3.Error as e:
        print("Database error:", e)


def change_position(old_position: int, new_position: int, commit=True):
    """
    Changes the position of a Todo object in the 'todos' table in the SQLite database.

    Args:
        old_position (int): The current position of the Todo object.
        new_position (int): The desired new position of the Todo object.
        commit (bool): Whether or not to commit the change to the database immediately.

    Returns:
        None
    """
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()


def update_todo(position: int, task: str, category: str):
    """
    Updates the task and/or category of a Todo object in the 'todos' table in the SQLite database.

    Args:
        position (int): The position of the Todo object to update.
        task (str): The new task string for the Todo object (or None to leave it unchanged).
        category (str): The new category string for the Todo object (or None to leave it unchanged).

    Returns:
        None
    """
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE todos SET task = :task, category = :category WHERE position = :position',
                      {'position': position, 'task': task, 'category': category})
        elif task is not None:
            c.execute


def complete_todo(position: int):
    """
    Sets the status of a Todo object at the given position to "completed" and updates the date_completed field to the
    current time.

    :param position: The position of the Todo object to complete.
    """
    with conn:
        COMPLETED_STATUS = 2
        c.execute('UPDATE todos SET status = ?, date_completed = ? WHERE position = ?', 
                 (COMPLETED_STATUS, datetime.datetime.now().isoformat(), position))
