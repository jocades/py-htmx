from dominate.tags import *


def component(name: str, age: int):
    print('imported component')
    return div(f'Hello {name}, age: {age}!')


def banner(**kwargs):
    print('imported banner')
    print(f'Hello {kwargs}!')
