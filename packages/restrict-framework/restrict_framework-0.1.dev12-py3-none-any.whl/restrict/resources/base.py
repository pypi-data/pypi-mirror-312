from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Effects:
    create: MutableMapping[str, Any] = field(default_factory=dict)
    modify: MutableMapping[str, Any] = field(default_factory=dict)
    delete: MutableMapping[str, Any] = field(default_factory=dict)


@dataclass
class Rules:
    list: dict[str, Any] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)
    accstar: dict[str, Any] = field(default_factory=dict)
    create: dict[str, Any] = field(default_factory=dict)
    modify: dict[str, Any] = field(default_factory=dict)
    delete: dict[str, Any] = field(default_factory=dict)
    mutstar: dict[str, Any] = field(default_factory=dict)
    listentry: bool = False
    detailsentry: bool = False


@dataclass
class CompiledResourceField:
    name: str


class CompiledResource(ABC):  # pragma: nocover
    def get_entry(self, name: str):
        for f in self.data:
            if f.name == name:
                return f
        for rel in self.dnc:
            if rel.name == name:
                return rel

    @property
    def override(self) -> str:
        return ""

    @property
    def prefix(self) -> str:
        if not hasattr(self, "_prefix"):
            self._prefix = ""
        return self._prefix

    @prefix.setter
    def prefix(self, value: Any):
        self._prefix = value

    @property
    def resolved_prefix(self) -> Any:
        if not hasattr(self, "_resolved_prefix"):
            self._resolved__prefix = ""
        return self._resolved_prefix

    @resolved_prefix.setter
    def resolved_prefix(self, value: Any):
        self._resolved_prefix = value

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def archetype(self) -> str:
        pass

    @property
    @abstractmethod
    def data(self) -> list:
        pass

    @property
    @abstractmethod
    def dnc(self) -> list:
        pass

    @property
    @abstractmethod
    def effects(self) -> Effects:
        pass

    @property
    @abstractmethod
    def security(self) -> Rules:
        pass

    @property
    @abstractmethod
    def globals(self) -> list[str]:
        pass


includes = []
resources = []
datatypes = {}
functions = {}
