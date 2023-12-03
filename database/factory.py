from abc import abstractmethod, ABCMeta
import sqlite3
from pydantic import BaseModel
from rich import print
from typing import Self, TypedDict, Unpack, Optional, NotRequired, Iterable, Generator, Optional, Union, Any, TypeVar
from contextlib import contextmanager, _GeneratorContextManager
from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(init=False)
    name: str

    def __post_init__(self):
        self.id = len(self.name)


u = User(name='John')
print(u.id)


class Model(BaseModel):
    ...


class Todo(Model):
    __table__ = 'todo'

    id: int | None = None
    title: str
    done: bool = False

    def __in__(self, title: str, done: bool = False):
        self.title = title
        self.done = done


# inspect all attrs and methods of a class
# print(inspect.getmembers(Todo, inspect.isfunction))
# print(inspect.getmembers(Todo, inspect.ismethod))


# def pydant(model: BaseModel, data: dict):
#     model.model_validate(data)
#
# pydant(TodoIn, {'title': 'Do something', 'done': False})


def row_factory(cursor, row, model) -> Todo:
    fields = [col[0] for col in cursor.description]
    return model(**dict(zip(fields, row)))


class QueryBuilder[T]:
    def __init__(
            self,
            con: sqlite3.Connection,
            cur: sqlite3.Cursor,
            model: T | None = None,
    ):
        self.con = con
        self.cur = cur
        self.table = ""
        self.sql = ""

        if model is not None:
            self.set_model(model)

    def select(
            self,
            model: T | None = None,
            fields: list[str] | None = None
    ):
        if model is not None:
            self.set_model(model)
        elif model is None and not self.table:
            raise Exception('No model or table set')

        return Select[T](self, fields)

    def insert(self, data: type[T]):
        return Insert[T](self, data)

    def set_model(self, model: T):
        self.table = getattr(model, '__table__', model.__name__.lower())
        self.cur.row_factory = lambda cursor, row: row_factory(cursor, row, model)


# SELECT + FROM + WHERE
# INSERT + INTO + VALUES
# UPDATE + SET + WHERE -> full update
# UPDATE + SET + WHERE -> partial update
# DELETE + FROM + WHERE


class Exec[T]:
    def __init__(self, qb: QueryBuilder[T]):
        self.qb = qb

    def all(self) -> list[T]:
        print(self.qb.sql)
        self.qb.cur.execute(self.qb.sql)
        self.qb.sql = ""
        return self.qb.cur.fetchall()

    def one(self) -> T:
        print(self.qb.sql)
        self.qb.cur.execute(self.qb.sql)
        self.qb.sql = ""
        return self.qb.cur.fetchone()


class Where[T](Exec[T]):
    def __init__(self, qb: QueryBuilder[T], sql: str, **kwargs):
        self.qb = qb
        self.qb.sql += f' WHERE {sql}'


class Select[T](Exec[T]):
    def __init__(self, qb: QueryBuilder[T], fields: list[str] | None = None):
        self.qb = qb
        self.qb.sql += f"SELECT {'*' if fields is None else ', '.join(fields)} FROM {qb.table}"

    def where(self, *args, **kwargs):
        return Where[T](self.qb, *args, **kwargs)

    def by_id(self, id: int) -> T:
        self.qb.sql += f' WHERE id = {id}'
        return self.one()


class Insert[T](Exec[T]):
    def __init__(self, qb: QueryBuilder[T], data: type[T]):
        self.qb = qb
        # get the keys and values from the object being passed in
        data = {k: v for k, v in data.model_dump().items() if v is not None}
        self.qb.sql += f"INSERT INTO {qb.table} ({', '.join(data.keys())}) VALUES ({', '.join(data.values())})"
        # self.qb.sql += f"INSERT INTO {qb.table} ({', '.join(data.keys())}) VALUES ({', '.join(data.values())})"

    def exec(self):
        print(self.qb.sql)
        # self.qb.cur.execute(self.qb.sql)
        # self.qb.con.commit()
        self.qb.sql = ""


type Schema = dict[str, type]


class Database:
    def __init__(self, db_name: str, schema: Schema | None):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.schema = schema

    @contextmanager
    def __call__[T](self,  model: T | None = None):
        yield QueryBuilder(self.con, self.cur, model)

    def query_builder[T](self, model: T):
        return QueryBuilder(self.con, self.cur, model)


# operators
def and_(*args: str):
    return ' AND '.join(args)


def or_(*args: str):
    return ' OR '.join(args)


def eq(f: str, v: str | int):
    return f'{f} = {v}'


def gt(f: str, v: int):
    return f'{f} > {v}'


def gte(f: str, v: int):
    return f'{f} >= {v}'


def lt(f: str, v: int):
    return f'{f} < {v}'


def lte(f: str, v: int):
    return f'{f} <= {v}'


def like(f: str, v: str):
    return f'{f} LIKE {v}'


db = Database('data.db', schema={'todo': Todo})

qb = db.query_builder(Todo)

with db(Todo) as q:
    todo = q.select().by_id(10)
    print(todo)

    data = Todo(title='Do something')
    # remove values which are None
    data = {k: v for k, v in data.model_dump().items() if v is not None}
    print(data)

    # q.insert(data).exec()


#
# todo = qb.select().where(eq('id', 1)).one()
# print(todo)
#
# todos = qb.select().where(and_(gt('id', 0), lt('id', 5))).all()
# print(todos)
#
# todos = qb.select().all()
# print(todos[1:5])


external_data = {
    "title": "Do something",
    "done": False

}
