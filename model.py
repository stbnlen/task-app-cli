import datetime
from dataclasses import dataclass


@dataclass
class Todo:
    """A todo item with a task, category, date added, date completed, status, and position.

    Attributes:
        task (str): The description of the todo item.
        category (str): The category of the todo item.
        date_added (str, optional): The date and time the todo item was created, in ISO format.
        date_completed (str, optional): The date and time the todo item was completed, in ISO format.
        status (int, optional): The status of the todo item. 1 = open, 2 = completed.
        position (int, optional): The position of the todo item in the list of todos.
    """

    task: str
    category: str
    date_added: str = None
    date_completed: str = None
    status: int = 1  # 1 = open, 2 = completed
    position: int = None

    def __post_init__(self):
        """Initializes the todo item with the current date and time if date_added is None."""
        if self.date_added is None:
            self.date_added = datetime.datetime.now().isoformat()
