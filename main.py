from fastapi import FastAPI, Request, Header, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from uvicorn import run
from random import randint
from sqlite3 import connect, Row
from rich import print
from pathlib import Path
import re

from dominate.tags import table, thead, tbody, tr, td, th
from typing import Generator

from web.dynamic.utils import HTMXResponse, render, HTMPY
from web.dynamic.todos import todo_row, todo_item


app = FastAPI()
con = connect('data.db')
c = con.cursor()


class Todo:
    title: str
    done: bool

    def __str__(self):
        return f'{self.title} {"[x]" if self.done else "[ ]"}'


def row_factory(row: Row, cls: type):
    obj = cls()
    setattr(obj, 'id', row[0])
    for i, field in enumerate(cls.__annotations__, 1):
        setattr(obj, field, row[i])
    return obj


htmpy = HTMPY('./web/pages')


# pages
@app.get('/', tags=['pages'], response_class=HTMLResponse)
async def root():
    data = c.execute('SELECT * FROM todo').fetchall()
    return htmpy(
        'home.html',
        todos=[todo_item(row_factory(row, Todo)) for row in data],
        todo_rows=[todo_row(row_factory(row, Todo)) for row in data]
    )


# api
@app.get('/random', tags=['api'])
async def random():
    return randint(0, 100)


@app.get('/todos', tags=['api'])
async def list_todos(hx_request: str | None = Header(None)):
    res = c.execute('SELECT * FROM todo LIMIT 5')
    todos = [row_factory(row, Todo) for row in res.fetchall()]
    if hx_request:
        return htmpy.fragment(
            tr(
                td(todo.id, cls='t-row'),
                td(todo.title, cls='t-row'),
                td(todo.done, cls='t-row'),
                cls='text-center text-gray-500'
            ) for todo in todos
        )
    return todos


@app.post('/todos', tags=['api'])
async def create_todo(title: str = Form(...)):
    c.execute('INSERT INTO todo (title, done) VALUES (?, ?)', (title, 0))
    con.commit()
    return htmpy.fragment(
        todo_row(row_factory(
            c.execute('SELECT * FROM todo WHERE id = ?', (c.lastrowid,)).fetchone(),
            Todo
        ))
    )


@app.post('/todos/{id}/toggle', tags=['api'])
async def toggle_todo_by_id(id: int):
    todo = row_factory(c.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone(), Todo)
    print(todo)
    todo.done = not todo.done
    c.execute('UPDATE todo SET done = ? WHERE id = ?', (todo.done, todo.id))
    con.commit()
    return HTMXResponse(todo_item(todo))


@app.delete('/todos/{id}', status_code=204, tags=['api'])
async def delete_todo_by_id(id: int):
    c.execute('DELETE FROM todo WHERE id = ?', (id,))
    con.commit()


if __name__ == '__main__':
    run('main:app', port=8000, reload=True, reload_includes='*.html')
