from __future__ import annotations

import dataclasses
import inspect
from collections import Counter
from collections.abc import Callable, MutableMapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Type, cast

from ...resources.base import CompiledResource
from ...resources.base import Effects as _EF
from ...resources.base import Rules as _R
from ...types.base import DataType

if TYPE_CHECKING:
    from .restrict import RestrictParser  # pragma: no cover


class FilePath:
    def __init__(self, *pathsegments: str | Path | FilePath):
        ps = [p._path if isinstance(p, FilePath) else p for p in pathsegments]
        self._path = Path(*tuple(ps))
        self._origabs = self._path.as_posix().startswith("/")

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return f"FilePath({self._path}, {self._origabs})"

    def __eq__(self, o):
        return self._path == o

    def __hash__(self):
        return hash(self._path)

    def __len__(self):
        return len(self._path.as_posix())

    def __truediv__(self, o) -> FilePath:
        p = FilePath(o / self._path)
        p._origabs = self._origabs
        return p

    def __rtruediv__(self, o) -> FilePath:
        p = FilePath(o / self._path)
        p._origabs = self._origabs
        return p

    def as_posix(self) -> str:
        return self._path.as_posix()

    def exists(self) -> bool:
        return self._path.exists()

    def open(self, *args, **kwargs):
        return self._path.open(*args, **kwargs)

    def resolve(self) -> FilePath:
        p = FilePath(self._path.resolve())
        p._origabs = self._origabs
        return p

    def with_suffix(self, s: str) -> FilePath:
        p = FilePath(self._path.with_suffix(s))
        p._origabs = self._origabs
        return p

    @property
    def origabs(self) -> bool:
        return self._origabs

    @property
    def parent(self) -> FilePath:
        p = FilePath(self._path.parent)
        p._origabs = self._origabs
        return p

    @property
    def stem(self) -> str:
        return self._path.stem

    @property
    def suffix(self) -> str:
        return self._path.suffix


BUILT_IN_TYPES = FilePath("/types/base")


@dataclass
class Modify:
    name: str
    prefix: str
    args: dict[str, Tx | Delete]
    resolved_prefix: FilePath | None = None


@dataclass
class Create:
    name: str
    prefix: str
    args: dict[str, Tx | Delete]
    resolved_prefix: FilePath | None = None


@dataclass
class Delete:
    pass


@dataclass
class Boolean:
    value: bool


@dataclass
class Int:
    value: int


@dataclass
class Float:
    value: float


@dataclass
class Str:
    value: str


@dataclass
class Ref:
    parts: list[str]

    def __getitem__(self, key):
        return self.parts[key]


@dataclass
class Tx:
    pipeline: Sequence[
        Create | Modify | Ref | Boolean | Int | Float | Str | Func | MappedFunc
    ]

    def __getitem__(self, key):
        return self.pipeline[key]


@dataclass
class Effects:
    create: MutableMapping[str, Tx | Delete]
    modify: MutableMapping[str, Tx | Delete]
    delete: MutableMapping[str, Tx | Delete]

    def merge(self, other: Effects | _EF):
        secs = ["create", "modify", "delete"]
        for sec in secs:
            od = getattr(other, sec)
            sd = getattr(self, sec)
            for key in od:
                if key not in sd:
                    sd[key] = deepcopy(od[key])


@dataclass
class MappedFunc:
    name: str
    prefix: str
    params: list[str]
    body: Tx
    resolved_prefix: FilePath | None = None


@dataclass
class Func:
    name: str
    prefix: str
    args: list[Ref | Int | Float | Boolean | Str | Tx]
    resolved_prefix: FilePath | None = None


@dataclass
class Field:
    name: str
    type: str
    prefix: str
    resolved_prefix: FilePath | None = None
    collection: str = ""
    constraint: Tx | None = None
    hidden: bool = False
    optional: bool = False
    readonly: bool = False
    computed: bool = False

    def to_rel(self, relation: str, multiplicity: int | Literal["*"]):
        return Rel(
            self.name,
            self.type,
            self.prefix,
            self.collection,
            relation,
            multiplicity,
            self.resolved_prefix,
            self.constraint,
            self.hidden,
            self.optional,
            self.readonly,
        )


@dataclass
class Rel:
    name: str
    type: str
    prefix: str
    collection: str
    relation: str
    multiplicity: int | Literal["*"]
    resolved_prefix: FilePath | None = None
    constraint: Tx | None = None
    hidden: bool = False
    optional: bool = False
    readonly: bool = False


@dataclass
class Rules:
    list: dict[str, Tx]
    details: dict[str, Tx]
    accstar: dict[str, Tx]
    create: dict[str, Tx]
    modify: dict[str, Tx]
    delete: dict[str, Tx]
    mutstar: dict[str, Tx]
    listentry: bool = False
    detailsentry: bool = False
    createentry: bool = False
    modifyentry: bool = False

    def merge(self, other: Rules | _R):
        secs = [
            "list",
            "details",
            "accstar",
            "create",
            "modify",
            "delete",
            "mutstar",
        ]
        for sec in secs:
            od = getattr(other, sec)
            sd = getattr(self, sec)
            for key in od:
                if key not in sd:
                    sd[key] = deepcopy(od[key])


Fields = list[Field]
Rels = list[Rel]


@dataclass
class Resource:
    archetype: str
    name: str
    prefix: str
    data: Fields
    dnc: Rels
    effects: Effects
    security: Rules
    resolved_prefix: FilePath | None = None
    override: str = ""

    def get_entry(self, name: str) -> Field | Rel | None:
        for field in self.data:
            if field.name == name:
                return field
        for rel in self.dnc:
            if rel.name == name:
                return rel

    def merge(self, other: Resource | CompiledResource) -> Resource:
        for entry in other.data:
            if self.get_entry(entry.name) is None:
                self.data.append(deepcopy(entry))
        for rel in other.dnc:
            if self.get_entry(rel.name) is None:
                self.dnc.append(deepcopy(rel))
                if rel.type == self.name:
                    self.dnc[-1].resolved_prefix = self.resolved_prefix
                    self.dnc[-1].prefix = self.prefix
        self.effects.merge(other.effects)
        self.security.merge(other.security)
        return self


@dataclass
class Include:
    path: FilePath
    alias: str


@dataclass
class File:
    includes: list[Include]
    resources: list[Resource]
    path: FilePath

    def set_resource(self, i: int, o: Resource):
        self.resources[i] = o

    def declares(self, name: str) -> bool:
        for resource in self.resources:
            if resource.name == name:
                return True
        return False

    def declares_func(self, _: str) -> bool:
        return False

    def get_declaration(self, name: str) -> Resource | None:
        for resource in self.resources:
            if resource.name == name:
                return resource

    def get_data_type(self, name: str) -> Type[DataType] | None:
        pass

    @property
    def absincludes(self):
        for incl in self.includes:
            if not incl.path.as_posix().startswith("/"):
                p = self.path.parent / incl.path.with_suffix(".resources")
                incl.path = p
            yield incl


@dataclass
class CompiledFile:
    includes: list[Include]
    _resources: list[Type[CompiledResource]]
    datatypes: dict[str, Type[DataType]]
    functions: dict[str, Callable]
    path: FilePath

    def set_resource(self, i: int, o: Resource):
        pass

    @property
    def resources(self):
        for res in self._resources:
            yield res()

    def declares(self, name: str) -> bool:
        if name in self.datatypes:
            return True
        for resource in self.resources:
            if resource.name == name:
                return True
        return False

    def declares_func(self, name: str) -> bool:
        return name in self.functions

    def get_declaration(
        self, name: str
    ) -> CompiledResource | Type[DataType] | None:
        if name in self.datatypes:
            return self.datatypes[name]
        for resource in self.resources:
            if resource.name == name:
                return resource

    def get_data_type(self, name: str) -> Type[DataType] | None:
        if name in self.datatypes:
            return self.datatypes[name]

    @property
    def absincludes(self):
        return []


class FileResolver:
    def resolve(
        self,
        parser: "RestrictParser",
        path: FilePath,
    ) -> CompiledFile | File | None:
        if path.origabs:
            if path.stem == "base":
                return None
            return self._resolve_compiled_file(path)
        else:
            if path.suffix == "":
                path = path.with_suffix(".resources")
            content = self.get_content(path)
            if content is None:
                return None
            return parser.parse(path.resolve(), content)

    def get_content(self, path: FilePath) -> str | None:
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    def _resolve_compiled_file(self, path: FilePath):
        mod_path = path.as_posix().replace("/", ".")
        mod = import_module("restrict" + mod_path)
        return CompiledFile(
            mod.includes,
            mod.resources,
            mod.datatypes,
            mod.functions,
            path,
        )


class RestrictError(Exception):
    def __eq__(self, o):
        return self.args == o.args


class AmbiguousTypeError(RestrictError):
    def __init__(self, name: str, possibilities: list[str | FilePath]):
        super().__init__(name, possibilities)


class DuplicateTypeError(RestrictError):
    pass


class MissingTypeError(RestrictError):
    def __init__(
        self,
        type: str,
        name: str,
        prefix: str,
        resolved_prefix: FilePath | None | Any,
        path: FilePath | None,
    ):
        super().__init__(type, name, prefix, resolved_prefix, path)


class MissingFunctionError(RestrictError):
    pass


class BadReferenceError(RestrictError):
    def __init__(self, missing_part: str, full_ref: str, path: FilePath | None):
        super().__init__(missing_part, full_ref, path)


class MissingOverrideProperty(RestrictError):
    def __init__(
        self, name: str, base: CompiledResource | Resource, override: Resource
    ):
        super().__init__(name, base, override)


@dataclass
class FileGraph:
    root: File
    resolver: FileResolver
    parser: "RestrictParser"
    files: dict[FilePath, File | CompiledFile | None] = dataclasses.field(
        default_factory=dict
    )
    errors: list[RestrictError] = dataclasses.field(default_factory=list)
    globals: dict[str, Resource] = dataclasses.field(default_factory=dict)

    def resolve(self):
        self.globals.clear()
        self.files.clear()

        self.files[BUILT_IN_TYPES] = self.resolver._resolve_compiled_file(
            BUILT_IN_TYPES
        )

        breadth: list[File | CompiledFile] = [self.root]
        errors: dict[FilePath, list] = {}
        self.files[self.root.path] = self.root

        # Resolve the tree of files
        while len(breadth) > 0:
            file = breadth.pop(0)
            for absincl in file.absincludes:
                if absincl.path in self.files:
                    continue
                file = self.resolver.resolve(self.parser, absincl.path)
                if file is None:
                    errors[absincl.path] = self.parser.errors
                    self.files[absincl.path] = None
                else:
                    self.files[absincl.path] = file
                    file.path = absincl.path
                    breadth.append(file)

        for path, file in self.files.items():
            if file is None or path.origabs:
                continue

            # Detect duplicate resource names in file
            resource_names = [r.name for r in file.resources]
            dup_resources = [
                k for k, v in Counter(resource_names).items() if v > 1
            ]
            for duplicate in dup_resources:
                error = DuplicateTypeError(duplicate, file.path)
                self.errors.append(error)

            for i, resource in enumerate(file.resources):
                if resource.prefix == "":
                    resource.resolved_prefix = file.path

                if not isinstance(resource, CompiledResource):
                    self._merge_overrides(resource, file, i)

            for i, resource in enumerate(file.resources):
                self._resolve_type_prefixes(file, resource.data)
                self._resolve_type_prefixes(file, resource.dnc)

                data_constraints = [
                    d.constraint
                    for d in resource.data
                    if d.constraint is not None
                ]
                self._resolve_tx_func_prefixes(file, data_constraints)
                if not isinstance(resource, CompiledResource):
                    self._resolve_tx_refs(file, resource, data_constraints)

                sec = resource.security
                sec_actions = [
                    sec.list,
                    sec.details,
                    sec.accstar,
                    sec.create,
                    sec.modify,
                    sec.delete,
                    sec.mutstar,
                ]
                for action in sec_actions:
                    values = list(action.values())
                    self._resolve_tx_func_prefixes(file, values)
                    if not isinstance(resource, CompiledResource):
                        self._resolve_tx_refs(file, resource, values)

                eff = resource.effects
                eff_actions = [eff.create, eff.modify, eff.delete]
                for action, section in zip(
                    eff_actions, ["create", "modify", "delete"]
                ):
                    values = list(action.values())
                    self._resolve_tx_func_prefixes(file, values)
                    if not isinstance(resource, CompiledResource):
                        self._resolve_tx_refs(file, resource, values)

                    # Ensure effects keys are in data or dnc
                    for attr in action.keys():
                        found = False
                        for f in resource.data:
                            if f.name == attr:
                                found = True
                                break
                        if not found:
                            for f in resource.dnc:
                                if f.name == attr:
                                    found = True
                                    break
                        if not found:
                            self.errors.append(
                                BadReferenceError(
                                    attr,
                                    f"{section}#{attr}",
                                    file.path,
                                )
                            )

    def _merge_overrides(
        self,
        resource: Resource,
        file: File | CompiledFile,
        i: int,
    ):
        if resource.override == "override":
            self._resolve_type_prefix(file, resource)
            res_source = self.files.get(FilePath(resource.override))
            if res_source is not None:
                source = res_source.get_declaration(resource.name)
                if source is not None and not inspect.isclass(source):
                    merged = resource.merge(source)
                    if isinstance(source, CompiledResource):
                        for global_ in source.globals:
                            entry = merged.get_entry(global_)
                            if entry is None:
                                error = MissingOverrideProperty(
                                    global_,
                                    source,
                                    resource,
                                )
                                self.errors.append(error)
                            self.globals[global_] = resource
                    file.set_resource(i, merged)

    def _resolve_tx_refs(
        self,
        file: File | CompiledFile,
        resource: Resource,
        coll: Sequence[Tx | Delete],
    ):
        for tx in coll:
            if isinstance(tx, Delete):
                continue
            for i, entry in enumerate(tx.pipeline):
                if isinstance(entry, Ref):
                    self._resolve_ref(resource, entry, file.path, i == 0)
                elif isinstance(entry, Func):
                    for j, arg in enumerate(entry.args):
                        if isinstance(arg, Ref):
                            self._resolve_ref(resource, arg, file.path, j == 0)

    def _resolve_ref(
        self,
        resource: Resource | None,
        ref: Ref,
        path: FilePath,
        is_first: bool,
    ):
        missing_part = ""
        file = self.files.get(path)
        if (
            is_first
            and len(ref.parts) == 1
            and (ref[0] == "value" or ref[0] == "_")
        ):
            return
        res: Resource | CompiledResource | None = resource
        if ref[0] in self.globals:
            res = self.globals[ref[0]]
        for i, part in enumerate(ref.parts):
            if file is None or res is None:
                missing_part = part
                break
            if i == 0 and (part == "self" or part == "selves"):
                continue
            else:
                entry = res.get_entry(part)
            if entry is None:
                missing_part = part
                break
            resolved_prefix = entry.resolved_prefix
            file = self.files.get(
                resolved_prefix
                if resolved_prefix is not None
                else BUILT_IN_TYPES
            )
            if file is not None:
                thing = file.get_declaration(entry.type)
                if not inspect.isclass(thing):
                    res = thing
            else:
                res = None
        if len(missing_part) > 0:
            error = BadReferenceError(
                missing_part,
                ".".join(ref.parts),
                path,
            )
            self.errors.append(error)

    def _resolve_tx_func_prefixes(
        self,
        file: File | CompiledFile,
        coll: Sequence[Tx | Delete],
    ):
        for tx in coll:
            if isinstance(tx, Delete):
                continue
            for entry in tx.pipeline:
                if isinstance(entry, Create) or isinstance(entry, Modify):
                    if len(entry.prefix) > 0:
                        for absincl in file.absincludes:
                            if absincl.alias == entry.prefix:
                                source = self.files[absincl.path]
                                if source is not None and source.declares(
                                    entry.name
                                ):
                                    entry.resolved_prefix = absincl.path
                                else:
                                    error = MissingTypeError(
                                        entry.name,
                                        "",
                                        entry.prefix,
                                        entry.resolved_prefix,
                                        file.path,
                                    )
                                    self.errors.append(error)
                    else:
                        possibilities = []
                        for absincl in file.absincludes:
                            if len(absincl.alias) > 0:
                                continue
                            source = self.files[absincl.path]
                            if source is not None and source.declares(
                                entry.name
                            ):
                                possibilities.append(absincl.path)
                        if len(possibilities) == 0:
                            error = MissingTypeError(
                                entry.name, "", "", None, file.path
                            )
                            self.errors.append(error)
                        elif len(possibilities) > 1:
                            error = AmbiguousTypeError(
                                entry.name, possibilities
                            )
                            self.errors.append(error)
                        else:
                            entry.resolved_prefix = possibilities[0]
                elif isinstance(entry, Func) or isinstance(entry, MappedFunc):
                    if len(entry.prefix) > 0:
                        for absincl in file.absincludes:
                            if absincl.alias == entry.prefix:
                                source = self.files[absincl.path]
                                if source is not None and source.declares_func(
                                    entry.name
                                ):
                                    entry.resolved_prefix = absincl.path
                                else:
                                    error = MissingFunctionError(
                                        entry.name,
                                        entry.prefix,
                                        str(absincl.path),
                                    )
                                    self.errors.append(error)
                    else:
                        if (
                            entry.name
                            in cast(
                                CompiledFile, self.files[BUILT_IN_TYPES]
                            ).functions
                        ):
                            entry.resolved_prefix = BUILT_IN_TYPES
                        else:
                            possibilities = []
                            for absincl in file.absincludes:
                                if len(absincl.alias) > 0:
                                    continue
                                source = self.files[absincl.path]
                                if source is not None and source.declares_func(
                                    entry.name
                                ):
                                    possibilities.append(absincl.path)
                            if len(possibilities) == 0:
                                error = MissingFunctionError(entry.name, "", "")
                                self.errors.append(error)
                            else:
                                entry.resolved_prefix = possibilities[0]

    def _resolve_type_prefixes(
        self,
        file: File | CompiledFile,
        coll: list[Field] | list[Rel],
    ):
        for entry in coll:
            self._resolve_type_prefix(file, entry)

    def _resolve_type_prefix(
        self,
        file: File | CompiledFile,
        entry: Field | Rel | Resource,
    ):
        if isinstance(entry, Resource):
            key = entry.name
            target = "override"
            check_current_file = False
            has_prefix = entry.resolved_prefix != file.path
        else:
            key = entry.type
            target = "resolved_prefix"
            check_current_file = True
            has_prefix = len(entry.prefix) > 0

        if key in cast(CompiledFile, self.files[BUILT_IN_TYPES]).datatypes:
            setattr(entry, target, BUILT_IN_TYPES)
        elif has_prefix:
            for absincl in file.absincludes:
                if absincl.alias == entry.prefix:
                    source = self.files[absincl.path]
                    if source is not None and source.declares(key):
                        setattr(entry, target, absincl.path)
                    else:
                        error = MissingTypeError(
                            key,
                            entry.name,
                            entry.prefix,
                            entry.resolved_prefix,
                            absincl.path,
                        )
                        self.errors.append(error)
        else:
            possibitities = []
            check_includes = True
            if check_current_file:
                value = file.get_declaration(key)
                if inspect.isclass(value):
                    return
                if value is not None and value.override != "":
                    # Don't check includes if this is an overridden
                    # resource
                    check_includes = False
                    possibitities.append(file.path)
                elif value is not None:
                    possibitities.append(file.path)
            if check_includes:
                for absincl in file.absincludes:
                    if len(absincl.alias) > 0:
                        continue
                    source = self.files[absincl.path]
                    if source is not None and source.declares(key):
                        possibitities.append(absincl.path)
            if len(possibitities) == 0:
                error = MissingTypeError(
                    key,
                    entry.name,
                    entry.prefix,
                    entry.resolved_prefix,
                    None,
                )
                self.errors.append(error)
            elif len(possibitities) > 1:
                error = AmbiguousTypeError(key, possibitities)
                self.errors.append(error)
            else:
                setattr(entry, target, possibitities[0])
