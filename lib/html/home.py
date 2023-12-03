from dominate import document
from dominate.tags import *
from pathlib import Path
import re
import imp
import sys

doc = document(title='Python + HTMX + Tailwind')

with doc.head:
    meta(charset='utf-8')
    meta(name='viewport', content='width=device-width, initial-scale=1')
    script(src='https://cdn.tailwindcss.com')
    script(src='https://unpkg.com/htmx.org@1.9.9')
    style('''
        @layer components {
            .btn {
                @apply bg-zinc-500 hover:bg-zinc-500/80 transition-colors duration-200 text-white py-2 px-4 rounded;
            }

            .t-row {
                @apply border border-gray-400 p-1;
            }
        }
        ''',
          type='text/tailwindcss'
          )

# generic functino to extend a tag and add a class


def component(tag: dom_tag, *args, **kwargs):
    cls = kwargs.get('cls', '')
    del kwargs['cls']
    return tag(*args, **kwargs, cls=f'{cls}')


# box = component(section, cls='flex flex-col items-center justify-center gap-2')


# wrapper for the section element
def box(*args, **kwargs):
    cls = kwargs.get('cls', '')
    del kwargs['cls']
    return section(*args, **kwargs, cls=f'flex flex-col items-center justify-center gap-2 {cls}')


with doc:
    with div(cls='bg-zinc-300'):
        with main(cls='relative flex flex-col min-h-screen py-8 container mx-auto space-y-20'):
            with box(cls='bg-red-200'):
                h1('Python + HTMX + Tailwind', cls='font-bold text-6xl tracking-tight')
                p(
                    'A ',
                    span('simple', cls='text-gray-600 font-semibold'),
                    ' example ',
                    span('without', cls='text-gray-600 font-semibold'),
                    ' a single line of ',
                    span('JavaScript', cls='text-gray-600 font-semibold'),
                    cls='text-lg text-gray-500'
                )
# print(doc)


def banner():
    return p(
        'A ',
        span('simple', cls='text-gray-600 font-semibold'),
        ' example ',
        span('without', cls='text-gray-600 font-semibold'),
        ' a single line of ',
        span('JavaScript', cls='text-gray-600 font-semibold'),
        cls='text-lg text-gray-500'
    )


# html = Path('./index.html').read_text(encoding='utf-8')
# html = html.format(content=banner())
# print(html)
