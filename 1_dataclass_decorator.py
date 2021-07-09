from marshmallow import Schema, fields
from marshmallow.schema import SchemaMeta


class MyMetaClass(SchemaMeta):

    def __new__(mcs, name, bases, classdict):
        for key in classdict:
            classdict[key] = Schema.TYPE_MAPPING[classdict[key]]()
        cls = super().__new__(mcs, name, bases, classdict)
        return cls


def my_dataclass(cls):
    types = cls.__annotations__

    def schema():
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
