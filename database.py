import sqlite3
from typing import List
from model import Todo
import datetime

conn = sqlite3.connect('todos.db')
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
            )""")


create_table()


def insert_todo(todo: Todo):
    """
    Inserts a Todo object into the 'todos' table in the SQLite database.

    Args:
        todo (Todo): The Todo object to insert.

    Returns:
        None
    """
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
        {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added,
         'date_completed': todo.date_completed, 'status': todo.status, 'position': todo.position })


def get_all_todos() -> List[Todo]:
    """
    Retrieves all Todo objects from the 'todos' table in the SQLite database.

    Returns:
        List[Todo]: A list of all Todo objects in the table.
    """
    c.execute('select * from todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def delete_todo(position):
    """
    Deletes a Todo object from the 'todos' table in the SQLite database at the specified position.

    Args:
        position (int): The position of the Todo object to delete.

    Returns:
        None
    """
    c.execute('select count(*) from todos')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from todos WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)


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
        c.execute('UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position',
                  {'position': position, 'date_completed': datetime.datetime.now().isoformat()})
