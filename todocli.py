# Define rules.
import sys

from turtle import width
from numpy import short
import typer 
from rich.console import Console
from rich.table import Table

sys.path.append('python-to-do-list-command-app/')
from models.database import delete_todo, get_all_todos, update_todo, complete_todo,insert_todo, init_db_table
from models.model import Todo


console = Console()

app = typer.Typer()

@app.command(short_help='add an item')
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task=task, category=category)
    insert_todo(todo)
    show()

@app.command(short_help='delete an item')
def detlete(id: int):
    typer.echo(f"deleting {id}")
    assert type(id) == int
    delete_todo(id)
    show()

@app.command(short_help='update an item')
def update(id: int, task: str=None, category: str=None):
    typer.echo(f"updating {id}")
    assert type(id) == int
    update_todo(id, task=task, category=category)
    show()

@app.command(short_help='complete an item')
def complete(id: int):
    typer.echo(f"complting {id}")
    assert type(id) == int

    complete_todo(id)
    show()

@app.command()
def show():
    tasks = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", '💻')

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    for idx, task in enumerate(tasks, start=1):
        color = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(task.id), task.task, f'[{color}]{task.category}[/{color}]', is_done_str)
    console.print(table)

def get_category_color(category):
    COLORS = {'Work': 'cyan', 'Video': 'red', 'Sports': 'cyan', 'Study': 'green'}
    if category in COLORS:
        return COLORS[category]
    return 'white'


if __name__ == '__main__':
    # init_db_table()
    app()
