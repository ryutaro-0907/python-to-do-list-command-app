from typing import List
from unicodedata import category 


from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


import datetime
from .model import Todo


engine = create_engine('sqlite:///todo.db', echo=True)

Session = sessionmaker(engine)

def insert_todo(todo:Todo):
    session = Session()

    try:
        session.add(todo)
        session.commit()
    finally:
        session.close()

def get_all_todos() -> List[Todo]:
    session = Session()
    try:
        todos = session.query(Todo).all()
        return todos
    except:
        metadata_obj = MetaData()
        todo = Table('todos', metadata_obj,
        # Column('id', Integer, primary_key=True),
        Column('task', String),
        Column('category', String),
        Column('date_added', String),
        Column('date_completed', String),
        Column('status', Integer)
        )
        todo.create(engine)
    
        example_todo = Todo(task='example task', category='example category')
        session.add(example_todo)
        session.commit()
        todos = session.query(Todo).all()
        return todos

    finally:
        session.close()

def delete_todo(todo_id:int):
    session = Session()

    try: 
        session.query(Todo).\
            filter(Todo.id==todo_id).\
                delete()
        session.commit()
    except:
        raise ValueError
    finally:
        session.close()


def update_todo(id:int, task:str=None, category:str=None):
    session = Session()

    try: 
        todo = session.query(Todo).\
            filter(Todo.id==id).\
                first()
        if task is not None and category is not None:
            todo.task = task
            todo.category = category
        elif task is not None:
            todo.task = task
        elif category is not None: 
            todo.category = category
        session.commit()
    except:
        raise ValueError
    finally:
        session.close()


def complete_todo(id:int):
    session = Session()
    try: 
        todo = session.query(Todo).\
            filter(Todo.id==id).\
                first()
        todo.status = 2
        todo.date_completed = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        session.commit()
    except:
        raise ValueError
    finally:
        session.close()


def init_db_table():
    metadata_obj = MetaData()
    todo = Table('todos', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('task', String),
    Column('category', String),
    Column('date_added', String),
    Column('date_completed', String),
    Column('status', Integer)
    )
    todo.create(engine)
    session = Session()


    example_todo = Todo(task='example task', category='example category')
    session.add(example_todo)
    session.commit()
    session.close()
   
    

