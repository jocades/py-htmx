from dominate.tags import *

from typing import Any
import re


class Todo:
    title: str
    done: bool

    def __init__(self, id: int, title: str, done: bool):
        self.id = id
        self.title = title
        self.done = done

    def __str__(self):
        return f'{self.title} {"[x]" if self.done else "[ ]"}'


def cn(*classes: str | dict[str, Any]) -> str:
    return ' '.join(
        cls if isinstance(cls, str)
        else ' '.join([k for k, v in cls.items() if v])
        for cls in classes
    )


def hx_attrs(attrs: dict[str, str]):
    '''
    hx_* -> data-hx-*
    x_* -> data-x-*
    '''
    x_attrs = {}
    for k, v in attrs.items():
        if k.startswith('hx_'):
            k = k.replace('hx_', 'data-hx-')
        elif k.startswith('x_'):
            k = k.replace('x_', 'data-x-')
        x_attrs[k] = v
    return x_attrs


def hx_element[T](element: T) -> T:
    def wrapper(*args, **kwargs):
        return element(*args, **hx_attrs(kwargs))   # type: ignore
    return wrapper  # type: ignore


elements = ['div', 'label', 'input_', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
            'span', 'a', 'button', 'img']

for element in elements:
    globals()[element] = hx_element(globals()[element])


def checkbox(*args, **kwargs):
    kwargs['type'] = 'checkbox'
    if kwargs.get('checked'):
        kwargs['checked'] = 'checked'
    return input_(*args, **kwargs)


def todo_item(todo: Todo):
    box = div(id=f'todo-{todo.id}', cls='flex px-4 py-2 rounded border border-gray-400 items-center justify-between')
    box.add(
        label(todo.title, cls=cn({'line-through text-gray-500': todo.done})),
        checkbox(
            name='done',
            hx_post=f'/todos/{todo.id}/toggle',
            # hx_target=f'#todo-{todo.id}',
            hx_target='closest div',
            hx_swap='outerHTML',
            checked=todo.done
        )
    )
    return box


def todo_row(todo: Todo):
    return tr(
        td(todo.id, cls='t-row'),
        td(todo.title, cls=cn('t-row', {'line-through text-gray-500': todo.done})),
        td(checkbox(
            hx_post=f'/todos/{todo.id}/toggle',
            hx_target=f'#todo-{todo.id}',
            hx_swap='outerHTML',
            checked=todo.done
        ), 
        button('X',
            hx_delete=f'/todos/{todo.id}',
            hx_target=f'#todo-{todo.id}',
            hx_swap='outerHTML',
            cls='text-red-500 ml-2' ),
        cls='t-row'),

        id=f'todo-{todo.id}',
        cls='text-center'
    )


@ table(id='todos', cls='p-2')
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
