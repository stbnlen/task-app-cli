# TodoApp - A Python CLI Todo List Application with Rich Console

TodoApp is a command-line interface (CLI) application written in Python, utilizing the Rich library for a rich console interface. It allows users to manage their todo items with the following commands:

- add: Add a new todo item.
- complete: Mark a todo item with a given position as complete.
- delete: Delete a todo item with a given position.
- show: Show all todo items in a table format.
- update: Update the task and/or category of a todo item with a given position.

## Installation

Clone the TodoApp repository to your local machine.

```
git clone git@github.com:stbnlen/task-app-cli.git
```

Navigate to the project directory.

```
cd task-app-cli
```

Install the required dependencies using pip.

```
pip install -r requirements.txt
```

## Usage

Use the available commands to manage your todo items.

### Show all todo items
```
todocli.py show
```

### Add a new todo item

```
todocli.py add <name> <category>
```

### Mark a todo item as complete
```
todocli.py complete <position>
```

### Delete a todo item
```
todocli.py delete <position>
```

### Update a todo item
```
todocli.py update <position> [--task <new_task>] [--category <new_category>]
```