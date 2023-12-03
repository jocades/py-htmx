import re
from pathlib import Path

# trying out this concept
# 'index.html'
# ---
# from fragments import component
# ---
# <!DOCTYPE html>
# ...
# {{ component }}


# then this functino will be called with the corred arguemnts needed to render the table

html = '''
---
from fragments import component
---

<!DOCTYPE html>
<body>
    {{ component }}

    {{ block 'fragments:component' }}

    <template id="fragments.component(name, age)">
</body>
'''


# html = Path('./html/index.html').read_text(encoding='utf-8')

# evaluate the code within the '---' delimiters
code = re.search(r'---\n(.*)\n---', html, re.DOTALL)
code = code.group(1) if code else ''

# for each line get the module and function name
rendered: str
for line in code.splitlines():
    module, func = line.split('from ')[1].split(' import ')
    print('IMPORT', module, func.split(','))
    for f in func.split(','):
        pass
        # mod = __import__(module)
        # fragment = getattr(mod, f.strip())

        # rendered = html.replace(f'{{{{ {f} }}}}', str(fragment(name='Jordi')))
        # render[f] = fragment


# remove the code from the html
rendered = re.sub(r'---\n.*\n---', '', html, re.DOTALL).strip()

# print(rendered)


# html = Path('./html/index.html').read_text(encoding='utf-8')

# now do the same but with the blocks
# get the module and function name
blocks = re.findall(r'{{ block \'(.*)\' }}', html)
for block in blocks:
    module, func = block.split(':')
    print('BLOCK', module, func)
    # mod = __import__(module)
    # fragment = getattr(mod, func)
    #
    # rendered = html.replace(f'{{{{ block \'{block}\' }}}}', str(fragment(name='Jordi')))

# print(rendered)


# now do the same but with the <template> tags
# get the module and function name
templates = re.findall(r'<template id="(.*)">', html)
# print(templates)
# t = 'fragments.component(todo)' # 'fragments = file, component = function, todo = kwargs'
kwargs = {'name': 'Jordi'}

for template in templates:
    module, func = template.split('.')
    print('TEMPLATE', module, func)

    # rendered = html.replace(f'<template id="{template}">', str(fragment(**kwargs)))
# print(rendered)
