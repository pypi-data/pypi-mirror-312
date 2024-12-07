from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any as TAny, Literal, Type, cast


class DataType(ABC):  # pragma: no cover
    value: TAny

    def __init__(self, value: TAny):
        pass

    @abstractmethod
    def json(self) -> int | str | float | dict | list | None:  # type: ignore
        pass

    def __eq__(self, other):
        return object.__eq__(self, other) is True or (
            self.__class__ == other.__class__ and self.value == other.value
        )

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


class BindingError(Exception):
    pass


class UnboundArgumentsError(Exception):
    def __init__(self, index: list[int] | int, message: str):
        super().__init__(index, message)


class Operator(ABC):  # pragma: nocover
    @abstractmethod
    def returns(self, args: Sequence[Type[DataType]]) -> Type[DataType] | None:
        pass

    @abstractmethod
    def num_args(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def bind(self, start_index: int, args: Sequence[DataType]):
        pass

    @abstractmethod
    def exec(self) -> DataType:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__


class NonaryOperator(Operator):
    def bind(self, start_index: int, args: Sequence[DataType]):
        raise BindingError(f"{self.name} can not bind any arguments", args)

    def num_args(self) -> tuple[int, int]:
        return (0, 0)

    def returns(self, args: Sequence[Type[DataType]]) -> Type[DataType] | None:
        if len(args) == 0:
            return self._returns()

    @abstractmethod
    def _returns(self) -> Type[DataType]:  # pragma: nocover
        pass


class UnaryOperator[T: DataType](Operator):
    def __init__(self):
        self._arg: T | None = None

    def bind(self, start_index: int, args: Sequence[DataType]):
        if len(args) != 1:
            raise BindingError(f"{self.name} can only bind one argument", args)
        if start_index != 0:
            raise BindingError(f"{self.name} can only bind to index 1")
        self._check_type(args[0])
        self._arg = cast(T, args[0])

    def exec(self) -> DataType:
        if self._arg is None:
            raise UnboundArgumentsError(
                0, f"{self.name} requires two arguments"
            )
        return self._op(self._arg)

    def num_args(self) -> tuple[int, int]:
        return (1, 1)

    def returns(self, args: Sequence[Type[DataType]]) -> Type[DataType] | None:
        if len(args) == 1:
            return self._returns(args[0])

    @abstractmethod
    def _check_type(self, arg: DataType):  # pragma: nocover
        pass

    @abstractmethod
    def _op(self, arg: T) -> DataType:  # pragma: nocover
        pass

    @abstractmethod
    def _returns(
        self, arg: Type[DataType]
    ) -> Type[DataType] | None:  # pragma: nocover
        pass


class BinaryOperator[S: DataType, T: DataType](Operator):
    def __init__(self):
        self._left: S | None = None
        self._right: T | None = None

    def bind(self, start_index: int, args: Sequence[DataType]):
        if len(args) > 1:
            raise BindingError(f"{self.name} can only bind one argument", args)
        if start_index > 1 or start_index < 0:
            raise BindingError(
                f"{self.name} can only bind to indexes 0 or 1", start_index
            )
        if start_index == 1:
            self._check_type(1, args[0])
            self._right = cast(T, args[0])
        elif start_index == 0:
            self._check_type(0, args[0])
            self._left = cast(S, args[0])

    def exec(self) -> DataType:
        if self._right is None and self._left is None:
            raise UnboundArgumentsError(
                [0, 1], f"{self.name} requires two arguments"
            )
        elif self._right is None:
            raise UnboundArgumentsError(
                1, f"{self.name} requires two arguments"
            )
        elif self._left is None:
            raise UnboundArgumentsError(
                0, f"{self.name} requires two arguments"
            )
        return self._op(self._left, self._right)

    def num_args(self) -> tuple[int, int]:
        return (2, 2)

    def returns(self, args: Sequence[Type[DataType]]) -> Type[DataType] | None:
        if len(args) == 2:
            return self._returns(args[0], args[1])

    @abstractmethod
    def _check_type(
        self, index: Literal[0, 1], arg: DataType
    ):  # pragma: nocover
        pass

    @abstractmethod
    def _op(self, left: S, right: T) -> DataType:  # pragma: nocover
        pass

    @abstractmethod
    def _returns(
        self, left: Type[DataType], right: Type[DataType]
    ) -> Type[DataType] | None:  # pragma: nocover
        pass


class ComparisonOperator(BinaryOperator[DataType, DataType]):
    def _check_type(self, index: Literal[0, 1], arg: DataType):
        if (
            self._left is not None
            and index == 1
            and self._left.__class__ != arg.__class__
        ) or (
            self._right is not None
            and index == 0
            and self._right.__class__ != arg.__class__
        ):
            raise ValueError(
                f"{self.name} requires two operands of the same type"
            )

    def _returns(
        self,
        left: Type[DataType],
        right: Type[DataType],
    ) -> Type[DataType] | None:
        if left == right:
            return Boolean


class _Boolean(DataType):
    value: bool

    def __init__(self, value: bool):
        self.value = value

    def json(self):
        return self.value

    def __str__(self):
        return "true" if self.value else "false"

    def __repr__(self):
        return "true" if self.value else "false"


TRUE = _Boolean(True)
FALSE = _Boolean(False)


class Boolean(DataType):
    def __new__(cls, value: str | bool):
        if value == "true" or value is True:
            return TRUE
        elif value == "false" or value is False:
            return FALSE
        else:
            raise ValueError("Boolean requires bool value or 'true' or 'false'")

    def json(self):
        raise RuntimeError("Cannot get JSON from Boolean")


class Empty(DataType):
    value: None

    def __init__(self):
        self.value = None

    def json(self):
        return None

    def __str__(self):
        return "null"

    def __repr__(self):
        return "null"


class Not(UnaryOperator[Boolean]):
    def _check_type(self, arg: DataType):
        if not isinstance(arg, _Boolean):
            raise ValueError("Not requires Boolean operand")

    def _op(self, arg: Boolean) -> DataType:
        return Boolean(not arg.value)

    def _returns(self, arg: Type[DataType]) -> Type[DataType] | None:
        if arg == Boolean:
            return Boolean


class Exists(UnaryOperator[DataType]):
    def _check_type(self, arg: DataType):
        return super()._check_type(arg)

    def _op(self, arg: DataType) -> DataType:
        if isinstance(arg, Empty):
            return FALSE
        return TRUE

    def _returns(self, arg: Type[DataType]) -> Type[DataType] | None:
        return Boolean


class And(BinaryOperator[Boolean, Boolean]):
    def _check_type(self, index: Literal[0, 1], arg: DataType):
        if not isinstance(arg, _Boolean):
            raise ValueError(f"{self.name} requires two Boolean operands")

    def _op(self, left: Boolean, right: Boolean) -> DataType:
        return TRUE if left == TRUE and right == TRUE else FALSE

    def _returns(
        self, left: Type[DataType], right: Type[DataType]
    ) -> Type[DataType] | None:
        if left is Boolean and right is Boolean:
            return Boolean


class Equals(ComparisonOperator):
    def _op(self, left: DataType, right: DataType) -> DataType:
        return TRUE if left.value == right.value else FALSE


class GreaterThan(ComparisonOperator):
    def _op(self, left: DataType, right: DataType) -> DataType:
        return TRUE if left.value > right.value else FALSE


class GreaterThanOrEqual(ComparisonOperator):
    def _op(self, left: DataType, right: DataType) -> DataType:
        return TRUE if left.value >= right.value else FALSE


class LessThan(ComparisonOperator):
    def _op(self, left: DataType, right: DataType) -> DataType:
        return TRUE if left.value < right.value else FALSE


class LessThanOrEqual(ComparisonOperator):
    def _op(self, left: DataType, right: DataType) -> DataType:
        return TRUE if left.value <= right.value else FALSE


class Or(BinaryOperator[Boolean, Boolean]):
    def _check_type(self, index: Literal[0, 1], arg: DataType):
        if not isinstance(arg, _Boolean):
            raise ValueError(f"{self.name} requires two Boolean operands")

    def _op(self, left: Boolean, right: Boolean) -> DataType:
        return TRUE if left == TRUE or right == TRUE else FALSE

    def _returns(
        self, left: Type[DataType], right: Type[DataType]
    ) -> Type[DataType] | None:
        if left is Boolean and right is Boolean:
            return Boolean


class CollectionOperator[T: DataType](Operator):
    def __init__(self):
        self._args: Sequence[T] | None = None

    def bind(self, start_index: int, args: Sequence[DataType]):
        if start_index != 0:
            raise BindingError(f"{self.name} can only bind to index 0")
        for arg in args:
            self._check_type(arg)
        if len(args) > 0:
            self._args = cast(Sequence[T], args)

    def exec(self) -> DataType:
        if self._args is None:
            raise UnboundArgumentsError(
                0, f"{self.name} requires 0 to 100 arguments"
            )
        return self._op(self._args)

    def num_args(self) -> tuple[int, int]:
        return (0, 100)

    def returns(self, args: Sequence[Type[DataType]]) -> Type[DataType] | None:
        if len(args) > self.num_args()[1]:
            return None
        for arg in args:
            if not self._returns(arg):
                return None
        return Boolean

    @abstractmethod
    def _check_type(self, arg: DataType):  # pragma: nocover
        pass

    @abstractmethod
    def _op(self, arg: Sequence[T]) -> DataType:  # pragma: nocover
        pass

    @abstractmethod
    def _returns(self, arg: Type[DataType]) -> bool:  # pragma: nocover
        pass


class Any(CollectionOperator[Boolean]):
    def _check_type(self, arg: DataType):
        if not isinstance(arg, _Boolean):
            raise ValueError("All requires Boolean arguments")

    def _op(self, arg: Sequence[Boolean]) -> DataType:
        for value in arg:
            if value == TRUE:
                return TRUE
        return FALSE

    def _returns(self, arg: Type[DataType]) -> bool:
        return arg is Boolean


class All(CollectionOperator[Boolean]):
    def _check_type(self, arg: DataType):
        if not isinstance(arg, _Boolean):
            raise ValueError("All requires Boolean arguments")

    def _op(self, arg: Sequence[Boolean]) -> DataType:
        for value in arg:
            if value == FALSE:
                return FALSE
        return TRUE

    def _returns(self, arg: Type[DataType]) -> bool:
        return arg is Boolean


class UnboundFunction:
    def __call__(self, **kwargs):
        pass


class Map:
    def __init__(self, params: list[str], func: UnboundFunction):
        self.func = func
        self.params = params

    def bind(self, args):
        if len(args) != len(self.params):
            raise ValueError(
                "Map got mismatched number of arguments for parameters"
            )
        self.args = [a if isinstance(a, tuple) else (a,) for a in args]

    def exec(self):
        return [
            self.func(**x)
            for x in [
                dict(x) for x in [zip(self.params, args) for args in self.args]
            ]
        ]


class Filter:
    def __init__(self, params: list[str], func: UnboundFunction):
        self.func = func
        self.params = params

    def bind(self, args):
        if len(args) != len(self.params):
            raise ValueError(
                "Map got mismatched number of arguments for parameters"
            )
        self.args = [a if isinstance(a, tuple) else (a,) for a in args]

    def exec(self):
        return [
            x
            for x in [
                dict(x) for x in [zip(self.params, args) for args in self.args]
            ]
            if self.func(**x)
        ]


class Zip:
    def __init__(self, params: list[str], func: UnboundFunction):
        self.func = func
        self.params = params

    def bind(self, args):
        if len(args) != 1 or (len(args) > 0 and not isinstance(args[0], list)):
            raise ValueError("Zip requires a list parameter")
        self.args = [a if isinstance(a, tuple) else (a,) for a in args]

    def exec(self):
        return [
            x
            for x in [
                dict(x) for x in [zip(self.params, args) for args in self.args]
            ]
            if self.func(**x)
        ]


includes = []
resources = []
datatypes = {
    "boolean": Boolean,
}
functions = {
    "and": And,
    "any": Any,
    "all": All,
    "eq": Equals,
    "exists": Exists,
    "filter": Filter,
    "gt": GreaterThan,
    "gte": GreaterThanOrEqual,
    "lt": LessThan,
    "lte": LessThanOrEqual,
    "map": Map,
    "not": Not,
    "or": Or,
    "zip": Zip,
}
