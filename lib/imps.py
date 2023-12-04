import re
from pathlib import Path


html = '''
---
from fragments import component
---
<html>
  <body>
    {{ component(name) }}

    {{ fragmnets.component(name) }}

    <fragment x-py="fragments.component(name)" />
    <fragment ="fragments.component(**kwargs)" />
  </body>
</html>
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


# THIS IS THE ONE!!!
# t = 'fragments.component(todo)' # 'fragments = file, component = function, todo = kwargs'
# add the possibily to grab blocks and fragments
test = '''
    # for n in range(3):
      <fragment x-py="fragments.component(name, age)" />
    # endfor

    <fragment x-py="fragments.component(name, age)" />
    <fragment id="fragments.component(**kwargs)" />


    {{ for todo in todos }}
    {{ block 'todo-row:todo' }}
      <tr>
        <td class="t-row">{{ todo.id }}</td>
        <td class="t-row">{{ todo.title }}</td>
        <td class="t-row">{{ todo.done }}</td>
      </tr>
    {{ endblock }}
    {{ endfor }}
'''

# parse the htmls to be able to loop 



kwargs = {'name': 'Jordi', 'age': 25}

# get the for loop  from the for to the ':'
for_loop = re.findall(r'# (.*):(.*)# endfor', test, re.DOTALL)
print(for_loop)
# evaluate the code
to_eval = for_loop[0][0].strip()
content = for_loop[0][1].strip()
print(to_eval)

# now for eahc one call the function with the kwargs


def get_content(html_fragment: str):
  module, func = html_fragment.split('.')
  func, args = func.split('(')
  args = args.replace(')', '').split(',')
  mod = __import__(module)
  fragment = getattr(mod, func)

  for arg in args:
    if arg.strip() in kwargs:
      kwargs[arg.strip()] = kwargs[arg.strip()]
    else:
      kwargs[arg.strip()] = ''
      
  return str(fragment(**kwargs))



exec(f'{to_eval}: ')



with_py = re.findall(r'<fragment x-py="(.*)" />', test)

for py in with_py:
  content = get_content(py)
  rendered = test.replace(f'<fragment x-py="{py}" />', content)
print(rendered)

# get the blocks, and replace them with the rendered html
# if the data givne is list, then render the block for each item

# blocks to be returned for htmx to consume, the 'x-py' attribute is the id being requested
# blocks = re.findall(r'<block x-py="(.*)">(.*)</block>', test, re.DOTALL)
# for block in blocks:
#     id, html = block
#     print('ID', id)
#     print('HTML', html)

# get the {{ block }} and {{ end }} and replace them with the rendered html
# the id is the name of the block which is in quotes
# blocks = re.findall(r'{{ block \'(.*)\' }}(.*){{ end }}', test, re.DOTALL)
# print(blocks)
#
# external_data = {
#     'todo-row': [{'id': 1, 'title': 'Buy milk', 'done': False},
#                  {'id': 2, 'title': 'Buy eggs', 'done': False}]
# }
#
# for block in blocks:
#     id, html = block
#     print('ID', id)
#     print('HTML', html)

# create a dict with the keys being the keys of the dict being passes
# i.e: {{ block 'todo-row' }} <tr> <td>{{ todo.id }}</td> </tr> {{ end }}
# todo-row = {'id': 1, 'title': 'Buy milk', 'done': False}


# kwargs = {'name': 'Jordi', 'age': 30}
# with_id = re.findall(r'<fragment id="(.*)" />', test)
#
# for id in with_id:
#     print(id)
#     module, func = id.split('.')
#     # remove the parenthesis get the func and then the args
#     func, args = func.split('(')
#     args = args.replace(')', '').split(',')
#     # get the args inside the '()' separated by ',' clean whitespace
#     print('ID', module, func, args)
#     mod = __import__(module)
#     fragment = getattr(mod, func)
#     for arg in args:
#         if arg.strip() in kwargs:
#             kwargs[arg.strip()] = kwargs[arg.strip()]
#
#     print(kwargs)
#     rendered = test.replace(f'<fragment id="{id}" />', str(fragment(**kwargs)))
# print(rendered)


# print(rendered)
