from datetime import datetime, timedelta, timezone
from typing import cast, Literal, Type
from .base import DataType, NonaryOperator, BinaryOperator


class Timestamp(DataType):
    value: datetime

    def __init__(self, value: str | datetime):
        if not isinstance(value, str) and not isinstance(value, datetime):
            raise ValueError(
                "Timestamp must be created from string or datetime"
            )
        if isinstance(value, str):
            self.value = datetime.fromisoformat(value)
        else:
            self.value = value
        if self.value.tzinfo is None:
            raise ValueError("Timestamp requires timezone information")

    def json(self):
        return self.value.isoformat()

    def __str__(self):
        return self.value.isoformat()

    def __repr__(self):
        return self.value.isoformat()


IntervalVal = tuple[int, int, int, int, int, int] | tuple[int]


class Interval(DataType):
    value: IntervalVal

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Interval requires a string object")
        self._original = value
        self.value = self._parse(value)

    def json(self):
        return f'"{str(self.value)}"'

    @staticmethod
    def _parse(value: str) -> IntervalVal:
        if value[0] != "P" or len(value) < 3:
            raise ValueError("Invalid interval format", value)
        if value[-1] == "W":
            return (int(value[1:-1]),)
        res = [0, 0, 0, 0, 0, 0]
        durations = ["Y", "M", "D"]
        times = ["H", "M", "S"]
        lookup = durations
        f = 1
        b = 1
        i = 0
        while f < len(value):
            if value[f] == "T":
                f += 1
                b = f
                lookup = times
                continue
            while value[f].isdigit():
                f += 1
            span = int(value[b:f])
            while i < len(res):
                if len(lookup) == 0:
                    raise ValueError("Invalid interval format", value)
                if lookup[0] == value[f]:
                    res[i] = span
                    i += 1
                    lookup.pop(0)
                    break
                else:
                    i += 1
                    lookup.pop(0)
            f += 1
            b = f
        return (res[0], res[1], res[2], res[3], res[4], res[5])

    def __str__(self):
        return self._original

    def __repr__(self):
        return self._original


class Now(NonaryOperator):
    def _returns(self) -> Type[Timestamp]:
        return Timestamp

    def exec(self) -> DataType:
        return Timestamp(datetime.now(timezone.utc))


class Add(BinaryOperator[Interval | Timestamp, Timestamp | Interval]):
    def _check_type(self, index: Literal[0, 1], arg: DataType):
        if not isinstance(arg, Interval) and not isinstance(arg, Timestamp):
            raise ValueError("Add requires Interval or Timestamp values")
        if self._compare_left(arg) or self._compare_right(arg):
            raise ValueError(
                "Add requires one Interval and one Timestamp value"
            )

    def _op(
        self, left: Interval | Timestamp, right: Interval | Timestamp
    ) -> DataType:
        interval = (
            left.value
            if isinstance(left, Interval)
            else cast(IntervalVal, right.value)
        )
        dt = (
            left.value
            if isinstance(left, Timestamp)
            else cast(datetime, right.value)
        )
        dttup = dt.timetuple()

        if len(interval) == 1:
            time_sum = dt + timedelta(days=21)
        else:
            res = tuple(x + y for x, y in zip(interval, dttup))
            time_sum = datetime(*res, tzinfo=dt.tzinfo)
        return Timestamp(time_sum)

    def _returns(
        self, left: Type[DataType], right: Type[DataType]
    ) -> Type[DataType] | None:
        if (left is Interval and right is Timestamp) or (
            left is Timestamp and right is Interval
        ):
            return Timestamp

    def _compare_left(self, arg) -> bool:
        return self._left is not None and self._left.__class__ == arg.__class__

    def _compare_right(self, arg) -> bool:
        return (
            self._right is not None and self._right.__class__ == arg.__class__
        )


includes = []
resources = []
datatypes = {"timestamp": Timestamp, "time_interval": Interval}
functions = {"now": Now, "time_add": Add}
