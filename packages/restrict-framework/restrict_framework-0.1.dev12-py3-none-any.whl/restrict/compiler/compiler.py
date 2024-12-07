from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Literal, Type

from .parsers.ast import FileGraph
from ..types.base import _Boolean, DataType, Empty


class JsonProvider(ABC):
    @abstractmethod
    def json(self) -> Any:  # pragma: nocover
        pass


class JsonException(Exception, JsonProvider):
    pass


class JsonWarning(Warning, JsonProvider):
    pass


class MissingPrefixError(Exception):
    def __init__(self, entry, resource):
        super().__init__(entry, resource)


class ResourceExceptionGroup(Exception):
    def __init__(
        self,
        exceptions: Sequence[JsonException],
        warnings: Sequence[JsonWarning],
    ):
        super().__init__(exceptions, warnings)

    @property
    def exceptions(self):
        return self.args[0]

    @property
    def warnings(self):
        return self.args[1]

    def json(self):
        return {
            "errors": [e.json() for e in self.exceptions],
            "warnings": [e.json() for e in self.warnings],
        }


class MissingFieldError(JsonException):
    def __init__(self, field_name: str, resource_name: str):
        super().__init__(field_name, resource_name)

    @property
    def field_name(self) -> str:
        return self.args[0]

    @property
    def resource_name(self) -> str:
        return self.args[1]

    def json(self):
        return {
            "pointer": f"/{self.field_name}",
            "title": "missing field",
            "detail": f"{self.field_name} is a required field for {self.resource_name}",
        }

    def __eq__(self, other):
        return other.__class__ is MissingFieldError and other.args == self.args


@dataclass(frozen=True)
class WritableDataFieldDef:
    owner: ResourceDefinition
    name: str
    type: Type[DataType]
    is_optional: bool
    is_hidden: bool
    validator: Callable[[dict], _Boolean]
    create_: Callable[[dict], DataType]

    @property
    def is_required(self):
        return not self.is_optional


@dataclass(frozen=True)
class ReadonlyDataFieldDef:
    owner: ResourceDefinition
    name: str
    type: Type[DataType]
    is_hidden: bool
    create_: Callable[[dict], DataType]

    @property
    def is_required(self):
        return False


@dataclass(frozen=True)
class ComputedDataFieldDef:
    owner: ResourceDefinition
    name: str
    type: Type[DataType]
    is_hidden: bool
    computation: Callable[[dict], DataType]

    @property
    def is_required(self):
        return False


@dataclass(frozen=True)
class DncFieldDef:
    owner: ResourceDefinition
    name: str
    multiplicity: int | Literal["*"]
    type: type[ResourceDefinition]
    is_optional: bool
    is_hidden: bool
    create_: Callable[[dict], ResourceInstance | None]

    @property
    def is_required(self):
        return not self.is_optional


class ResourceDefinition:
    fields: dict[
        str,
        WritableDataFieldDef
        | ReadonlyDataFieldDef
        | ComputedDataFieldDef
        | DncFieldDef,
    ]

    def __init__(self, name: str):
        self.name = name
        self.fields = {}

    def add_writable_data_field(
        self,
        name: str,
        type: type[DataType],
        is_optional: bool,
        is_hidden: bool,
        validator: Callable[[dict], _Boolean],
        create_: Callable[[dict], DataType],
    ):
        field = WritableDataFieldDef(
            self, name, type, is_optional, is_hidden, validator, create_
        )
        self._add_field(field)

    def add_readonly_data_field(
        self,
        name: str,
        type: Type[DataType],
        is_hidden: bool,
        create_: Callable[[dict], DataType],
    ):
        field = ReadonlyDataFieldDef(self, name, type, is_hidden, create_)
        self._add_field(field)

    def add_computed_data_field(
        self,
        name: str,
        type: Type[DataType],
        is_hidden: bool,
        computation: Callable[[dict], DataType],
    ):
        field = ComputedDataFieldDef(self, name, type, is_hidden, computation)
        self._add_field(field)

    def add_dnc_field(
        self,
        name: str,
        multiplicity: int | Literal["*"],
        type: type[ResourceDefinition],
        is_optional: bool,
        is_hidden: bool,
        create_: Callable[[dict], ResourceInstance | None],
    ):
        field = DncFieldDef(
            self, name, multiplicity, type, is_optional, is_hidden, create_
        )
        self._add_field(field)

    def create(self, data: dict[str, Any]):
        for field_name, field in self.fields.items():
            if (
                not isinstance(field, ComputedDataFieldDef)
                and field_name not in data
            ):
                default_value = field.create_(data)
                if default_value is not None and not isinstance(
                    default_value, Empty
                ):
                    data[field_name] = default_value
        missing_fields_errors = [
            MissingFieldError(field.name, self.name)
            for field in self.fields.values()
            if field.is_required and field.name not in data
        ]
        if len(missing_fields_errors) > 0:
            raise ResourceExceptionGroup(missing_fields_errors, [])

    def _add_field(
        self,
        field: (
            WritableDataFieldDef
            | ReadonlyDataFieldDef
            | ComputedDataFieldDef
            | DncFieldDef
        ),
    ):
        if field.name in self.fields:
            raise KeyError(field.name, field)
        self.fields[field.name] = field


class DataField:
    pass


class ReadonlyDataField:
    pass


class ComputedDataField:
    pass


class ResourceInstance:
    pass


class RestrictCompiler:
    def __init__(self, graph: FileGraph):
        self.graph = graph

    def compile(self) -> tuple[Sequence[ResourceDefinition]]:
        root = self.graph.root

        runnable_resources = []
        # for resource in root.resources:
        #     fields = []
        #     for entry in resource.data:
        #         if entry.resolved_prefix is None:
        #             raise MissingPrefixError(entry, resource)
        #         file = self.graph.files.get(entry.resolved_prefix)
        #         if file is None:
        #             raise MissingPrefixError(entry, resource)
        #         entry_type = file.get_data_type(entry.type)
        #         if entry_type is None:
        #             raise MissingTypeError(
        #                 entry.type,
        #                 entry.name,
        #                 entry.prefix,
        #                 entry.resolved_prefix,
        #                 root.path,
        #             )
        #         field = RunnableResourceField(
        #             entry.name, entry_type, lambda x: (TRUE, [])
        #         )
        #         fields.append(field)
        #     cls = type(resource.name, (RunnableResource,), {})
        #     runnable_resources.append(cls(fields))

        return (runnable_resources,)
