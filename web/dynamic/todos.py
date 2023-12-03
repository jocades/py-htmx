from dominate.tags import table, thead, tbody, tr, td, th, _input, div, label


class Todo:
    title: str
    done: bool

    def __init__(self, id: int, title: str, done: bool):
        self.id = id
        self.title = title
        self.done = done

    def __str__(self):
        return f'{self.title} {"[x]" if self.done else "[ ]"}'

# {% for todo in todos %}
# <tr class="text-center text-gray-500">
#   <td class="t-row">{{ todo.id }}</td>
#   <td class="t-row">{{ todo.title }}</td>
#   <td class="t-row">
#     <input
#       name="done"
#       type="checkbox"
#       hx-post="/todos/{{ todo.id }}/toggle"
#       {%
#       if
#       todo.done
#       %}
#       checked
#       {%
#       endif
#       %}
#     />
#   </td>
# </tr>
# {% endfor %}


def todo_item(todo: Todo):
    input_e = _input(
        name='done',
        _type='checkbox',
        data_hx_post=f'/todos/{todo.id}/toggle',
        data_hx_target=f'#todo-{todo.id}',
        data_hx_swap='outerHTML',
    )

    if todo.done:
        input_e['checked'] = 'checked'

    return div(
        label(todo.title, cls=f'{'line-through text-gray-500' if todo.done else ''}'),
        input_e,
        id=f'todo-{todo.id}',
        cls='flex px-4 py-2 rounded border border-gray-400 items-center justify-between'
    )


def todo_row(todo: Todo):
    return tr(
        td(todo.id, cls='t-row'),
        td(todo.title, cls='t-row'),
        td(todo.done, cls='t-row'),
        cls='text-center text-gray-500'
    )


@table(id='todos', cls='p-2')
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
