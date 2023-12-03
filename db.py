import sqlite3
from rich import print
from collections import namedtuple
from pydantic import BaseModel
from typing import TypeVar, Type


# con = sqlite3.connect('data.db')
# cur = con.cursor()


sql_types = {
    'int': 'INTEGER',
    'str': 'TEXT',
    'float': 'REAL',
    'bool': 'INTEGER',
}


py_types = {
    'INTEGER': int,
    'TEXT': str,
    'REAL': float,
    'BOOLEAN': bool,
}


def py_to_sql(cls: type):
    return {
        field: field_type.__name__
        for field, field_type in cls.__annotations__.items()
    }


def sql_to_py(cls: type):
    return {
        field: py_types[field_type]
        for field, field_type in cls.__annotations__.items()
    }


# make this functino generic type so that it returns the correc ttype
def row_factory(row: sqlite3.Row, cls: Type[T] | None = None) -> T | sqlite3.Row:
    if not cls:
        return row

    obj = cls()
    setattr(obj, 'id', row[0])
    for i, field in enumerate(cls.__annotations__, 1):
        setattr(obj, field, row[i])
    return obj


class DataBase:
    con: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def get_cursor(self):
        return self.cur

    def query(
        self,
        sql: str,
        args: tuple = (),
        cls: type | None = None,
        single: bool = False,
    ):
        res = self.cur.execute(sql, args)
        if single:
            return row_factory(res.fetchone(), cls)
        return [row_factory(row, cls) for row in res.fetchall()]

    def exec(self, sql: str, args: tuple = (), returning: type | None = None):
        self.cur.execute(sql, args)
        self.con.commit()
        if returning:
            return row_factory(self.cur.fetchone(), returning)

    def exec_many(self, sql: str, args: list[tuple]):
        self.cur.executemany(sql, args)
        self.con.commit()

    def create_table(self, cls: type):
        sql_fields = ', '.join(
            f'{field} {sql_types[field_type]}'
            for field, field_type in py_to_sql(cls).items()
        )
        table_name = getattr(cls, '__table__', cls.__name__.lower())

        sql = f'CREATE TABLE {table_name} ('

        if not hasattr(cls, 'id'):
            sql += 'id INTEGER PRIMARY KEY AUTOINCREMENT, '

        sql += sql_fields + ');'

        print('sql:', sql)

        self.cur.execute(sql)


db = DataBase('data.db')


class TodoDb(BaseModel):
    id: int
    title: str
    done: bool


# from row to pydantic model


class Todo:
    title: str
    done: bool

    def __str__(self):
        return f'{self.title} {"[x]" if self.done else "[ ]"}'


c = db.get_cursor()

c.execute('SELECT * FROM todo')
res = c.fetchall()


todo = db.exec('INSERT INTO todo (title, done) VALUES (?, ?)', ('Walk the dog', 0), returning=Todo)


data = [
    ('Walk the dog', 0),
    ('Buy milk', 0),
    ('Do homework', 1),
    ('Do laundry', 0),
    ('Clean room', 0),
    ('Do dishes', 0),
    ('Take out trash', 0),
    ('Go to the gym', 0),
    ('Go to the store', 0),
    ('Go to the bank', 0),
    ('Go to the post office', 0),
    ('Go to the doctor', 0),
    ('Go to the dentist', 0),
]

# db.exec_many('INSERT INTO todo (title, done) VALUES (?, ?)', data)

todos = db.query('SELECT * FROM todo WHERE done = 1 LIMIT 5', cls=Todo)
print(list(map(str, todos)))


# construuct the values for the sql create tabel statement
def field(name: str, type: type, pk: bool = False, fk: bool = False, ref: str | None = None):
    sql = f'{name} {sql_types[str(type)]}'

    if pk:
        sql += ' PRIMARY KEY'

    if fk:
        sql += f' REFERENCES {ref}'

    return sql


def create():
    todo = Todo()

    # todo.__annotations__[field](row[i])


class TodoP(BaseModel):
    title: str
    done: bool

    def __str__(self):
        return f'{self.title} {"✅" if self.done else "❌"}'


new_todo = {
    'title': 'test',
    'done': 0,
}

todo = TodoP(**new_todo)

print(todo)


def sql_row_factory(cur, row):
    todo = Todo()
    setattr(todo, 'id', row[0])
    for i, field in enumerate(todo.__annotations__, 1):
        # call the type to convert the value
        setattr(todo, field, row[i])

    return todo


# con.row_factory = sql_row_factory
#
# res = cur.execute('SELECT * FROM todo')
# data = res.fetchall()
#
# print(list(map(str, data)))
