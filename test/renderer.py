import re
from pydantic import BaseModel

test = '''
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


test = '''
  <div>
    {{ range .todos }}
    {{ block 'todo-row' }}}
      <tr>
        <td class="t-row">{{ .id }}</td>
        <td class="t-row">{{ .title }}</td>
        <td class="t-row">{{ .done }}</td>
      </tr>
      {{ end }}
    {{ end }}
  </div>
'''

class Todo(BaseModel):
    id: int
    title: str
    done: bool

    def __str__(self):
        return f'{self.title} {"[x]" if self.done else "[ ]"}'


todos = [
    Todo(id=1, title='Buy milk',done= False),
    Todo(id=2, title='Buy bread',done= False),
]

kwargs = { 'todos': todos }

# find all the blocks that start with {{ range }}
range_blocks = re.findall(r'{{ range (.*?) }}(.*?){{ end }}', test, re.DOTALL)
print(range_blocks[0][0])

key = range_blocks[0][0]

for todo in kwargs[key]:
    print(todo)
    print(range_blocks[0][1])
    # replace the block with the data
    for k, v in todo.__dict__.items():
        print(k, v)
        range_blocks[0][1] = range_blocks[0][1].replace(f'{{{{ {k} }}}}', str(v))
    print(range_blocks[0][1])
















# get the for loop  from the for to the ':'
# blocks = re.findall(r'# (.*):(.*)# endfor', test, re.DOTALL)
# print(blocks)
# # evaluate the code
# to_eval = blocks[0][0].strip()
# for_block = blocks[0][1].strip()
# print(to_eval)

# iter = to_eval.split()[-1]
# item = to_eval.split()[1]

# render =''

# for todo in kwargs[iter]:
#     for k, v in todo.__dict__.items():
#         name = todo.__class__.__name__.lower() 
#         print(item, k, v)
#         for_block = for_block.replace(f'{{{{ {name}.{k} }}}}', str(v))
#     render += for_block
  
# print(render)


    
# # get any part of the html and pass it dat
# named_blocks = re.findall(r'{{ block \'(.*)\' }}(.*){{ endblock }}', test, re.DOTALL)

# data = Todo(id=1, title='Buy milk',done= False)

# for name, block in named_blocks:
#     print(name, block)
#     # replace the block with the data
#     for k, v in data.__dict__.items():
#         block = block.replace(f'{{{{ {k} }}}}', str(v))
#     print(block)
    








# for todo in todos:
#     print(content.replace(key, 'todo'))




# now for eahc one call the function with the kwargs







