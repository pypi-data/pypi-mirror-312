from typing import Literal, Type

from .base import BinaryOperator, DataType


class Int(DataType):
    value: int

    def __init__(self, value: str | int):
        if (
            not isinstance(value, str) and not isinstance(value, int)
        ) or isinstance(value, bool):
            raise ValueError(value)
        self.value = int(value)

    def json(self):
        return self.value


class Add(BinaryOperator[Int, Int]):
    def _returns(
        self, left: Type[DataType], right: Type[DataType]
    ) -> Type[DataType] | None:
        if left == Int and right == Int:
            return Int

    def _check_type(self, index: Literal[0, 1], arg: DataType):
        if not isinstance(arg, Int):
            raise ValueError(f"Arg {index} must be of type Int")

    def _op(self, left: Int, right: Int) -> DataType:
        return Int(left.value + right.value)


includes = []
resources = []
datatypes = {"int": Int, "integer": Int}
functions = {"add": Add}
