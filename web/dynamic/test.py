from dominate.tags import table, thead, tbody, tr, td, th, _input
from dominate.tags import dom_tag
from dominate.util import text
from typing import Generator, Optional, Union, Any, Callable, Awaitable, TypeVar, Generic
from fastapi.responses import HTMLResponse

from pathlib import Path


class Todo:
    title: str
    done: bool

    def __init__(self, id: int, title: str, done: bool):
        self.id = id
        self.title = title
        self.done = done

    def __str__(self):
        return f'{self.title} {"[x]" if self.done else "[ ]"}'


todos = [
    Todo(id=1, title='todo 1', done=False),
    Todo(id=2, title='todo 2', done=True),
]


def render(elements: dom_tag | list[dom_tag] | Generator[dom_tag, None, None]):
    if isinstance(elements, list) or isinstance(elements, Generator):
        return ''.join(str(e).strip() for e in elements)
    return str(elements).strip()


def todo_row(todo: Todo):
    return tr(
        td(todo.id, cls='t-row'),
        td(todo.title, cls='t-row'),
        td(todo.done, cls='t-row'),
        cls='text-center text-gray-500'
    )


@table(id='todos', cls='border p-2 rounded')
def todo_table(todos: list[Todo]):
    with thead(cls='text-lg font-semibold'):
        tr(
            th('id', cls='t-row'),
            th('title', cls='t-row'),
            th('done', cls='t-row'),
        )
    with tbody():
        for todo in todos:
            todo_row(todo)


# create a file in the current directory with the contect of the todo_table function
# Path('./todo_table.html').write_text(render(todo_table(todos)), encoding='utf-8')
