from typing import List

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


import datetime
from .model import Todo


class TodoManager:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///todo.db", echo=True)

        Session = sessionmaker(self.engine)
        self.session = Session()

    def insert_todo(self, todo: Todo):

        try:
            self.session.add(todo)
            self.session.commit()
        finally:
            self.session.close()

    def get_all_todos(self) -> List[Todo]:
        try:
            todos = self.session.query(Todo).all()
            return todos
        except:
            raise ValueError
        finally:
            self.session.close()

    def delete_todo(self, todo_id: int):
        try:
            self.session.query(Todo).filter(Todo.id == todo_id).delete()
            self.session.commit()
        except:
            raise ValueError
        finally:
            self.session.close()

    def update_todo(self, id: int, task: str = None, category: str = None):
        try:
            todo = self.session.query(Todo).filter(Todo.id == id).first()
            if task is not None and category is not None:
                todo.task = task
                todo.category = category
            elif task is not None:
                todo.task = task
            elif category is not None:
                todo.category = category
            self.session.commit()
        except:
            raise ValueError
        finally:
            self.session.close()

    def complete_todo(self, id: int):
        try:
            todo = self.session.query(Todo).filter(Todo.id == id).first()
            todo.status = 2
            todo.date_completed = str(datetime.datetime.today().strftime("%Y-%m-%d"))
            self.session.commit()
        except:
            raise ValueError
        finally:
            self.session.close()

    def init_db_table(self):
        metadata_obj = MetaData()
        todo = Table(
            "todos",
            metadata_obj,
            Column("id", Integer, primary_key=True),
            Column("task", String),
            Column("category", String),
            Column("date_added", String),
            Column("date_completed", String),
            Column("status", Integer),
        )
        todo.create(self.engine)

        example_todo = Todo(task="example task", category="example category")
        self.session.add(example_todo)
        self.session.commit()
        self.session.close()
