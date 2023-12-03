from dominate.tags import *


def component(name):
    print('imported component')
    return div(f'Hello {name}!')


def banner(**kwargs):
    print('imported banner')
    print(f'Hello {kwargs}!')
