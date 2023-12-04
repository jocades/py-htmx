from dominate.tags import dom_tag
from typing import Generator, Optional, Union, Any, Callable, Awaitable, TypeVar, Generic
from fastapi.responses import HTMLResponse
from pathlib import Path
import re


def render(elements: dom_tag | list[dom_tag] | Generator[dom_tag, None, None]):
    if isinstance(elements, list) or isinstance(elements, Generator):
        return ''.join(str(e).strip() for e in elements)
    return str(elements).strip()


def load_file(path: str | Path):
    return Path(path).read_text(encoding='utf-8')


class HTMXResponse(HTMLResponse):
    def __init__(
            self,
            content: str | dom_tag | list[dom_tag] | Generator[dom_tag, None, None],
            status_code: int = 200,
            headers: dict | None = None,
            media_type: str | None = None
    ):
        super().__init__(
            content if isinstance(content, str) else render(content),
            status_code,
            headers,
            media_type
        )
        self.headers['HX-Trigger'] = 'true'


def parse_html(html: str, **kwargs) -> str:
    with_py = re.findall(r'<fragment x-py="(.*)" />', html)

    for py in with_py:
        print(py)
        module, func = py.split('.')
        # remove the parenthesis get the func and then the args
        func, args = func.split('(')
        args = args.replace(')', '').split(',')
        # get the args inside the '()' separated by ',' clean whitespace
        print('PY', module, func, args)
        mod = __import__(f'web.dynamic.{module}', fromlist=[func])
        fragment = getattr(mod, func)

        # match the args with the kwargs
        for arg in args:
            if arg.strip() in kwargs:
                kwargs[arg.strip()] = kwargs[arg.strip()]
            else:
                kwargs[arg.strip()] = ''

        print(kwargs)
        html = html.replace(f'<fragment x-py="{py}" />', str(fragment(**kwargs)))

    return html


class HTMPY:
    def __init__(self, path: str):
        self.path = Path(path)

    def __call__(self, file: str, **kwargs):
        html = load_file(self.path / file)

        for key, value in kwargs.items():
            if not isinstance(value, str):
                value = render(value)

            html = html.replace(f'{{{{ {key} }}}}', value)

        return HTMLResponse(html)

    def fragment(
            self,
            content: str | dom_tag | Generator[dom_tag, None, None] | list,
            status_code: int = 200,
            headers: dict | None = None,
            media_type: str | None = None
    ):
        return HTMXResponse(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type
        )


# now for every element do this
