import re
# import all tags from dominate and crate my own tags
from dominate.tags import html_tag, div
from functools import wraps
import copy
from typing import Callable


def cn(classes: dict[str, bool]) -> str:
    return ' '.join([cls for cls, cond in classes.items() if cond])


def hx_attrs(attrs: dict[str, str]):
    return {re.sub(r'^hx_', 'data-hx-', k): v for k, v in attrs.items()}


def hx_element[T](element: T) -> T:
    def wrapper(*args, **kwargs):
        return element(*args, **hx_attrs(kwargs))   # type: ignore
    return wrapper  # type: ignore


my_div = hx_element(div)
print(my_div(id='my-div', hx_post='/todos', hx_target='#todos', hx_swap='outerHTML'))

my_div = hx_element(div)
