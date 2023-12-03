from typing import TypedDict, Unpack, Optional, NotRequired, Iterable
from pydantic import BaseModel


def gen[T](x: T) -> T:
    return x


n = gen(1)


class Kwargs(TypedDict):
    name: str
    age: NotRequired[int]


def profile(**kwargs: Unpack[Kwargs]) -> None:
    for k, v in kwargs.items():
        print(f"{k}: {v}")


class Employee:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def say_hello(self) -> None:
        print(f"Hello, {self.name}")


class Manager(Employee):
    ...


def get_employees():
    yield Employee("John", 30)
    yield Manager("Jane", 40)


def get_one[T](iterable: Iterable[T]) -> Optional[T]:
    return next(iter(iterable), None)


class Todo(BaseModel):
    id: int
    title: str


# decoratro to automatically convert dict to Todo
def parse(func):
    def wrapper(todo):
        return func(Todo.model_validate(todo))
    return wrapper


def parse_from(model):
    def decorator(func):
        def wrapper(**kwargs):
            return func(model.model_validate(kwargs))
        return wrapper
    return decorator


# convert todo type to dict type param
class TodoDict(TypedDict):
    id: int
    title: str


data = {"id": 1, "title": "hello"}

todo = Todo.model_validate(data)
print(todo)

# create_todo(id=1 , title="hello")

if __name__ == "__main__":
    profile(name="John", age=30)

    data = list(get_employees())
    john = data[0]
    john.say_hello()

    one = get_one(data)
    print(one)
