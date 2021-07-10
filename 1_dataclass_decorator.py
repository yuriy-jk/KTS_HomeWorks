from marshmallow import Schema
from marshmallow.schema import SchemaMeta
from typing import Any, Callable, TypeVar, Dict

ClassUser = TypeVar('ClassUser')


class MyMetaClass(SchemaMeta):

    def __new__(mcs, name: str, bases: tuple, classdict: Dict):
        for key in classdict:
            classdict[key] = Schema.TYPE_MAPPING[classdict[key]]()
        cls = super().__new__(mcs, name, bases, classdict)
        return cls


def my_dataclass(cls: Any) -> Callable:
    """
    decorator for User
    build User.Scheme class
    validate User's annotaions fields with marsmallow.schema fields
    """

    types = cls.__annotations__

    def schema() -> ClassUser:
        cls.Schema = MyMetaClass('User', (Schema,), types)
        return cls

    return schema()


@my_dataclass
class User:
    username: str
    age: int
    superuser: bool


print(User.Schema)
print(User.Schema().load({'username': 'tod', 'age': 18}))
print(User.Schema().load({'username': 'tod', 'age': 18, 'superuser': False}))
