import re
import random
import string
from typing import Type
from .base import DataType, UnaryOperator
from .scalar import Int


class Text(DataType):
    value: str

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Text must have str or bytes value")
        self.value = value

    def json(self):
        return self.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class Email(Text):
    """Email#check regex from http://emailregex.com"""

    value: str
    check = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def __init__(self, value: str):
        super().__init__(value)
        if not self.check.match(value):
            raise ValueError("Email must have valid email value")


class Password(Text):
    value: str

    def __init__(self, value: str):
        super().__init__(value)
        if len(value) == 0:
            raise ValueError("Password cannot be empty")


class Reverse(UnaryOperator[Text]):
    def _check_type(self, arg: DataType):
        if not isinstance(arg, Text):
            raise ValueError("Reverse requires a Text value")

    def _op(self, arg: Text):
        return arg.__class__("".join(reversed(arg.value)))

    def _returns(self, arg: Type[DataType]) -> Type[DataType] | None:
        if issubclass(arg, Text):
            return arg


class Len(UnaryOperator[Text]):
    def _check_type(self, arg: DataType):
        if not isinstance(arg, Text):
            raise ValueError("Len requires a Text value")

    def _op(self, arg: Text):
        return Int(len(arg.value))

    def _returns(self, arg: Type[DataType]) -> Type[DataType] | None:
        if issubclass(arg, Text):
            return arg


class RandomString(UnaryOperator[Int]):
    def _check_type(self, arg: DataType):
        if not isinstance(arg, Int):
            raise ValueError("RandomString requires a Int value")

    def _op(self, arg: Int):
        return Text(
            "".join(
                random.choice(string.ascii_letters) for i in range(arg.value)
            )
        )

    def _returns(self, arg: Type[DataType]) -> Type[DataType] | None:
        if issubclass(arg, Int):
            return Text


includes = []
resources = []
datatypes = {
    "text": Text,
    "email": Email,
    "password": Password,
}
functions = {
    "reverse": Reverse,
    "len": Len,
    "random_string": RandomString,
}
