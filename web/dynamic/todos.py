from dominate.tags import table, thead, tbody, tr, td, th, _input, div, label
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


def cn(classes: dict[str, bool]) -> str:
    return ' '.join([cls for cls, cond in classes.items() if cond])


# converter function to transrom any element passed from dominate to transform any atrribute that starts with hx_ to
# data-hx-*
def hx_attrs(attrs: dict[str, str]):
    return {re.sub(r'^hx_', 'data-hx-', k): v for k, v in attrs.items()}


# wrapper to transrom any dominate element and accept hx_ attributes
def hx_element(element):
    def wrapper(*args, **kwargs):
        return element(*args, **hx_attrs(kwargs))

    return wrapper


my_div = hx_element(div)
print(my_div(id='my-div', hx_post='/todos', hx_target='#todos', hx_swap='outerHTML'))

# now for every element do this


def checkbox(*args, **kwargs):
    kwargs['type'] = 'checkbox'
    if kwargs.get('checked', False):
        kwargs['checked'] = 'checked'
    return _input(*args, **kwargs)


def todo_item(todo: Todo):
    box = div(id=f'todo-{todo.id}', cls='flex px-4 py-2 rounded border border-gray-400 items-center justify-between')
    box.add(
        label(todo.title, cls=cn({'line-through text-gray-500': todo.done})),
        checkbox(
            name='done',
            data_hx_post=f'/todos/{todo.id}/toggle',
            data_hx_target=f'#todo-{todo.id}',
            data_hx_swap='outerHTML',
            checked=todo.done
        )
    )
    return box


def todo_row(todo: Todo):
    return tr(
        td(todo.id, cls='t-row'),
        td(todo.title, cls='t-row'),
        td(todo.done, cls='t-row'),
        cls='text-center text-gray-500'
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
