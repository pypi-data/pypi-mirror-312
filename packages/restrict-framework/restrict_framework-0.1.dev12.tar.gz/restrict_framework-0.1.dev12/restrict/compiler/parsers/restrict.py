import functools
import inspect
from collections.abc import Generator
from itertools import permutations
from typing import Literal

from ..lexers.restrict import RestrictLexer
from ..ply.yacc import LRParser, yacc
from .ast import (
    Boolean,
    Create,
    Delete,
    Effects,
    Field,
    Fields,
    File,
    FilePath,
    Float,
    Func,
    Include,
    Int,
    MappedFunc,
    Modify,
    Ref,
    Rels,
    Resource,
    Rules,
    Str,
    Tx,
)

FieldName = str
FieldPrefix = str
FieldCollectionType = str


def RULE(
    first_line_or_gen: str | Generator[str, None, None] | None,
    *args: str,
):
    if first_line_or_gen is None:
        raise SyntaxError("Cannot create a RULE with no specification")

    def set_doc(func):
        @functools.wraps(func)
        def wrapper(self, p):
            return func(self, p)

        lines: list[str] = []
        if isinstance(first_line_or_gen, list):
            lines = first_line_or_gen
        elif inspect.isgenerator(first_line_or_gen):
            lines = list(first_line_or_gen) + list(args)
        elif isinstance(first_line_or_gen, str):
            lines = [first_line_or_gen] + list(args)
        rule_name = func.__name__[2:]
        wrapper.__doc__ = (
            rule_name
            + " : "
            + ("\n" + " " * len(rule_name) + " | ").join(lines)
        )
        return wrapper

    return set_doc


class RestrictParser:
    _parser: LRParser | None = None
    _lexer: RestrictLexer | None = None
    _debug: bool = False

    start = "file"

    @classmethod
    def dump_rules(cls, file_name: str = "rules.out"):
        with open(file_name, "w") as f:
            for attr_name in dir(cls):
                if not attr_name.startswith("p_"):
                    continue
                attr = getattr(cls, attr_name)
                if attr.__doc__ is None:
                    continue
                print(attr.__doc__, "\n", file=f)

    def __init__(self):
        self._errors = []

    @property
    def errors(self):
        return [x for x in self._errors]

    @property
    def tokens(self) -> list[str]:
        if self._lexer is None:
            return []
        print("TOKENS", self._lexer.tokens)
        return self._lexer.tokens

    def build(self, debug=False, tracking=False) -> "RestrictParser":
        self._debug = debug
        self._tracking = tracking
        self._lexer = RestrictLexer().build(debug=debug)
        self._parser = yacc(module=self, debug=debug)
        return self

    def parse(self, path: FilePath, input: str) -> File | None:
        if len(input.strip()) == 0:
            return File([], [], path)
        if self._parser is None:
            raise NameError("You must build the parser first")
        self._errors = []
        result = self._parser.parse(
            input, lexer=self._lexer, tracking=self._tracking
        )
        if result is not None:
            includes, declarations = result
            result = File(includes, declarations, path)
        return result

    def p_error(self, p):
        print("Syntax error in input", p)
        self._errors.append(p)
        if self._debug:
            raise SyntaxError(p)

    @RULE("")
    def p_empty(self, _):
        pass

    ####################################################################
    # FILE
    @RULE(
        "use_stmt opt_use_stmts",
        "use_stmt opt_use_stmts resource opt_resources",
        "resource opt_resources",
    )
    def p_file(self, p) -> tuple[list[Include], list[Resource]]:
        if isinstance(p[1][0], Include):
            uses = p[1] + p[2]
            resources = [] if len(p) == 3 else p[3] + p[4]
        else:
            uses = []
            resources = p[1] + p[2]
        p[0] = (uses, resources)
        return p[0]

    # FILE
    ####################################################################

    ####################################################################
    # USE STATEMENTS
    @RULE(
        "USE PATH",
        "USE PATH ID",
    )
    def p_use_stmt(self, p) -> list[Include]:
        p[0] = [Include(FilePath(p[2]), "" if len(p) == 3 else p[3])]
        return p[0]

    @RULE(
        "use_stmt opt_use_stmts",
        "empty",
    )
    def p_opt_use_stmts(self, p) -> list[Include]:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    # USE STATEMENTS
    ####################################################################

    ####################################################################
    # TOP-LEVEL RESOURCE AND SECTION DECLARATIONS
    @RULE(
        "RESTYPE RESNAME '{' sections '}'",
        "OVERRIDE RESTYPE RESNAME '{' sections '}'",
        "OVERRIDE RESTYPE ID '.' RESNAME '{' sections '}'",
    )
    def p_resource(self, p) -> list[Resource]:
        if p[4] == ".":
            restype = p[2]
            prefix = p[3]
            resname = p[5]
        else:
            restype = p[len(p) - 5]
            prefix = ""
            resname = p[len(p) - 4]
        override = "override" if p[1] == "override" else ""
        data, dnc, eff, sec = p[len(p) - 2]

        p[0] = [
            Resource(
                restype, resname, prefix, data, dnc, eff, sec, None, override
            )
        ]
        return p[0]

    @RULE(
        "resource opt_resources",
        "empty",
    )
    def p_opt_resources(self, p) -> list[Resource]:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE(
        " ".join(y)
        for x in [
            list(permutations(["data", "dnc", "effects", "security"], n))
            for n in range(1, 5)
        ]
        for y in x
    )
    def p_sections(self, p) -> tuple[Fields, Rels, Effects, Rules]:
        sections = [
            [],
            [],
            Effects({}, {}, {}),
            Rules({}, {}, {}, {}, {}, {}, {}),
        ]
        for section in p[1:]:
            match section[0]:
                case "data":
                    sections[0] = section[1]
                case "dnc":
                    sections[1] = section[1]
                case "effects":
                    sections[2] = section[1]
                case "security":
                    sections[3] = section[1]
        p[0] = tuple(sections)
        return p[0]

    # TOP-LEVEL RESOURCE AND SECTION DECLARATIONS
    ####################################################################

    ####################################################################
    # DATA SECTION
    @RULE(
        "DATA '{' data_field opt_data_fields '}'",
        "DATA '{' computed_field opt_data_fields '}'",
    )
    def p_data(self, p) -> tuple[str, Fields]:
        p[0] = ("data", p[3] + p[4])
        return p[0]

    @RULE(
        "valid_field_id ':' opt_field_mods data_field_type ';'",
        "valid_field_id ':' opt_field_mods data_field_type opt_constraint ';'",
    )
    def p_data_field(self, p) -> Fields:
        field_name = p[1]
        name, prefix, collection_type = p[4]
        mods = p[3]
        constraint = p[len(p) - 2] if len(p) > 6 else None
        p[0] = [
            Field(
                field_name,
                name,
                prefix,
                None,
                collection_type,
                constraint,
                *mods,
            )
        ]
        return p[0]

    @RULE(
        "data_field opt_data_fields",
        "computed_field opt_data_fields",
        "empty",
    )
    def p_opt_data_fields(self, p) -> Fields:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE(
        "'<' COMPUTED '>' valid_field_id ':' opt_field_mods data_field_type  ':' arg ';'",
    )
    def p_computed_field(self, p) -> Fields:
        field_name = p[4]
        name, prefix, collection_type = p[7]
        mods = p[6]
        mods[-1] = True
        constraint = p[len(p) - 2] if len(p) > 6 else None
        p[0] = [
            Field(
                field_name,
                name,
                prefix,
                None,
                collection_type,
                constraint,
                *mods,
            )
        ]
        return p[0]

    @RULE(
        "LIST ID '.' RESNAME",
        "LIST RESTYPE '.' RESNAME",
        "LIST ID '.' ID",
        "LIST RESTYPE '.' ID",
        "LIST RESNAME",
        "LIST ID",
        "SET ID '.' RESNAME",
        "SET RESTYPE '.' RESNAME",
        "SET ID '.' ID",
        "SET RESTYPE '.' ID",
        "SET RESNAME",
        "SET ID",
        "ID '.' RESNAME",
        "RESTYPE '.' RESNAME",
        "ID '.' ID",
        "RESTYPE '.' ID",
        "RESNAME",
        "ID",
    )
    def p_data_field_type(
        self, p
    ) -> tuple[FieldName, FieldPrefix, FieldCollectionType]:
        collection_type = ""
        name = ""
        prefix = ""

        name = p[len(p) - 1]
        if p[1] in ["list", "set"]:
            collection_type = p[1]
            if len(p) == 5:
                prefix = p[2]
        elif len(p) == 4:
            prefix = p[1]

        p[0] = (name, prefix, collection_type)
        return p[0]

    # DATA SECTION
    ####################################################################

    ####################################################################
    # DNC SECTION
    @RULE("DNC '{' rel opt_rels '}'")
    def p_dnc(self, p) -> tuple[str, Rels]:
        p[0] = ("dnc", p[3] + p[4])
        return p[0]

    @RULE(
        "'<' DESCTYPE '>' dnc_field",
        "'<' DNCDIR ':' mult '>' dnc_field",
        "'<' RESTYPE ':' mult '>' dnc_field",
        "'<' DETAILS ':' mult '>' dnc_field",
    )
    def p_rel(self, p) -> Rels:
        relation = p[2]
        multiplicity = p[4] if p[3] == ":" else 1
        p[0] = [p[len(p) - 1][0].to_rel(relation, multiplicity)]
        return p[0]

    @RULE(
        "INT",
        "'*'",
    )
    def p_mult(self, p) -> Int | Literal["*"]:
        p[0] = p[1]
        return p[0]

    @RULE(
        "rel opt_rels",
        "empty",
    )
    def p_opt_rels(self, p) -> Rels:
        p[0] = [] if len(p) == 2 else p[1] + p[2]
        return p[0]

    @RULE(
        "valid_field_id ':' opt_field_mods dnc_field_type ';'",
        "valid_field_id ':' opt_field_mods dnc_field_type opt_constraint ';'",
    )
    def p_dnc_field(self, p) -> Fields:
        field_name = p[1]
        name, prefix, collection_type = p[4]
        mods = p[3]
        constraint = p[len(p) - 2] if len(p) > 6 else None
        p[0] = [
            Field(
                field_name,
                name,
                prefix,
                None,
                collection_type,
                constraint,
                *mods,
            )
        ]
        return p[0]

    @RULE(
        "LIST ID '.' RESNAME",
        "LIST RESTYPE '.' RESNAME",
        "LIST RESNAME",
        "SET ID '.' RESNAME",
        "SET RESTYPE '.' RESNAME",
        "SET RESNAME",
        "ID '.' RESNAME",
        "RESTYPE '.' RESNAME",
        "RESNAME",
    )
    def p_dnc_field_type(
        self, p
    ) -> tuple[FieldName, FieldPrefix, FieldCollectionType]:
        collection_type = ""
        name = ""
        prefix = ""

        name = p[len(p) - 1]
        if p[1] in ["list", "set"]:
            collection_type = p[1]
        elif len(p) == 4:
            prefix = p[1]

        p[0] = (name, prefix, collection_type)
        return p[0]

    # DNC SECTION
    ####################################################################

    ####################################################################
    # EFFECTS SECTION

    @RULE("EFFECTS '{' effect_sections '}'")
    def p_effects(self, p) -> tuple[str, Effects]:
        p[0] = ("effects", Effects(**p[3]))
        return p[0]

    @RULE(
        " ".join(y)
        for x in [
            list(
                permutations(
                    ["create_effect", "modify_effect", "delete_effect"], n
                )
            )
            for n in range(1, 4)
        ]
        for y in x
    )
    def p_effect_sections(self, p) -> tuple[dict[str, dict[str, Tx | Delete]]]:
        sections = {"create": {}, "modify": {}, "delete": {}}
        for section in p[1:]:
            sections[section[0]] = section[1]
        p[0] = sections
        return p[0]

    @RULE("CREATE '{' effect opt_effects '}'")
    def p_create_effect(self, p) -> tuple[str, dict[str, Tx | Delete]]:
        p[0] = ("create", p[3] | p[4])
        return p[0]

    @RULE("MODIFY '{' effect opt_effects '}'")
    def p_modify_effect(self, p) -> tuple[str, dict[str, Tx | Delete]]:
        p[0] = ("modify", p[3] | p[4])
        return p[0]

    @RULE("DELETE '{' effect opt_effects '}'")
    def p_delete_effect(self, p) -> tuple[str, dict[str, Tx | Delete]]:
        p[0] = ("delete", p[3] | p[4])
        return p[0]

    @RULE(
        "valid_field_id ':' expr opt_effect_pipeline ';'",
        "valid_field_id ':' DELETE ';'",
    )
    def p_effect(self, p) -> dict[str, Tx | Delete]:
        if p[3] == "delete":
            p[0] = {p[1]: Delete()}
        else:
            p[0] = {p[1]: Tx([p[3]] + p[4])}
        return p[0]

    @RULE(
        # Normal functions
        "PIPEOP effect_func opt_effect_pipeline",
        "PIPEOP CREATE data_field_type '{' '}'",
        "PIPEOP CREATE data_field_type '{' effect opt_effects '}'",
        "PIPEOP MODIFY data_field_type '{' '}'",
        "PIPEOP MODIFY data_field_type '{' effect opt_effects '}'",
        "empty",
    )
    def p_opt_effect_pipeline(self, p) -> list[Func | MappedFunc | Create]:
        if len(p) > 4:
            name, prefix, _ = p[3]
            if len(p) == 6:
                args = {}
            else:
                args = p[5] | p[6]
            ctor = Create if p[2] == "create" else Modify
            p[0] = [ctor(name, prefix, args)]
        else:
            p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        # Normal functions
        "ID '(' ')'",  # 4
        "ID '.' ID '(' ')'",  # 6
        "ID '(' arg opt_args ')'",  # 6
        "ID '.' ID '(' arg opt_args ')'",  # 8
        # Mapped functions
        "ID '[' ID opt_params ']' '(' ID opt_properties opt_effect_pipeline ')'",  # 11
        "ID '.' ID '[' ID opt_params ']' '(' ID opt_properties opt_effect_pipeline ')'",  # 13
    )
    def p_effect_func(self, p) -> Func | MappedFunc:
        match (len(p), p[2], p[4] if len(p) > 4 else None):
            case (4, _, _):
                p[0] = Func(p[1], "", [])
            case (6, ".", "("):
                p[0] = Func(p[3], p[1], [])
            case (6, _, _):
                p[0] = Func(p[1], "", [p[3]] + p[4])
            case (8, ".", _):
                p[0] = Func(p[3], p[1], [p[5]] + p[6])
            case (_, "[", _):
                p[0] = MappedFunc(
                    p[1],
                    "",
                    [p[3]] + p[4],
                    Tx([Ref([p[7]] + p[8])] + p[9]),
                )

            case (_, ".", "["):
                p[0] = MappedFunc(
                    p[3],
                    p[1],
                    [p[5]] + p[6],
                    Tx([Ref([p[9]] + p[10])] + p[11]),
                )

        return p[0]

    @RULE(
        "effect opt_effects",
        "empty",
    )
    def p_opt_effects(self, p) -> dict[str, Tx]:
        p[0] = {} if len(p) == 2 else p[1] | p[2]
        return p[0]

    # EFFECTS SECTION
    ####################################################################

    ####################################################################
    # SECURITY SECTION

    @RULE(
        "SECURITY '{' mutators '}'",
        "SECURITY '{' accessors '}'",
        "SECURITY '{' mutators accessors '}'",
        "SECURITY '{' accessors mutators '}'",
    )
    def p_security(self, p) -> tuple[str, Rules]:
        if len(p) == 5:
            directives = p[3]
        else:
            directives = p[3] | p[4]
        for key, field in Rules.__dataclass_fields__.items():
            if key not in directives:
                directives[key] = False if field.type == "bool" else {}
        p[0] = ("security", Rules(**directives))
        return p[0]

    @RULE(
        (
            x
            for y in [
                (
                    f"MUTATORS '{{' {s} '}}'",
                    f"MUTATORS '{{' {s} secstar '}}'" if len(s) < 20 else "",
                )
                for s in [
                    " ".join(x)
                    for n in range(1, 4)
                    for x in permutations(
                        ["mutcreate", "mutmodify", "mutdelete"], n
                    )
                ]
            ]
            for x in y
            if len(x) > 0
        ),
        "MUTATORS '{' secstar '}'",
    )
    def p_mutators(self, p) -> dict[str, Tx]:
        d = {}
        for section in p[3 : len(p) - 1]:
            name = "mutstar" if section[0] == "*" else section[0]
            tx = section[-1]
            d[name] = tx
            if section[1] is True:
                d[name + "entry"] = True
        p[0] = d
        return p[0]

    @RULE("opt_entrypoint CREATE secdef")
    def p_mutcreate(self, p) -> tuple[Literal["create"], bool, dict[str, Tx]]:
        p[0] = ("create", p[1], p[3])
        return p[0]

    @RULE("opt_entrypoint MODIFY secdef")
    def p_mutmodify(self, p) -> tuple[Literal["modify"], bool, dict[str, Tx]]:
        p[0] = ("modify", p[1], p[3])
        return p[0]

    @RULE("DELETE secdef")
    def p_mutdelete(self, p) -> tuple[Literal["delete"], bool, dict[str, Tx]]:
        p[0] = ("delete", False, p[2])
        return p[0]

    @RULE(
        "ACCESSORS '{' secstar '}'",
        "ACCESSORS '{' acclist '}'",
        "ACCESSORS '{' acclist secstar '}'",
        "ACCESSORS '{' accdets '}'",
        "ACCESSORS '{' accdets secstar '}'",
        "ACCESSORS '{' accdets acclist '}'",
        "ACCESSORS '{' acclist accdets '}'",
    )
    def p_accessors(self, p) -> dict[str, Tx]:
        d = {}
        for section in p[3:-1]:
            name = "accstar" if section[0] == "*" else section[0]
            tx = section[-1]
            d[name] = tx
            if section[0] == "list" and section[1] is True:
                d["listentry"] = True
            elif section[0] == "details" and section[1] is True:
                d["detailsentry"] = True
        p[0] = d
        return p[0]

    @RULE("opt_entrypoint DETAILS secdef")
    def p_accdets(self, p) -> tuple[Literal["details"], bool, dict[str, Tx]]:
        p[0] = ("details", p[1], p[3])
        return p[0]

    @RULE("opt_entrypoint LIST secdef")
    def p_acclist(self, p) -> tuple[Literal["list"], bool, dict[str, Tx]]:
        p[0] = ("list", p[1], p[3])
        return p[0]

    @RULE("'*' secdef")
    def p_secstar(self, p) -> tuple[Literal["*"], dict[str, Tx]]:
        p[0] = ("*", p[2])
        return p[0]

    @RULE(
        "'{' security_field opt_security_fields  '}'",
        "':' expr opt_pipeline ';'",
    )
    def p_secdef(self, p) -> dict[str, Tx]:
        if isinstance(p[2], dict):
            p[0] = p[2] | p[3]
        else:
            p[0] = {"*": Tx([p[2]] + p[3])}
        return p[0]

    @RULE(
        "valid_field_id ':' expr opt_pipeline ';'",
        "'*' ':' expr opt_pipeline ';' ",
    )
    def p_security_field(self, p) -> dict[str, Tx]:
        p[0] = {p[1]: Tx([p[3]] + p[4])}
        return p[0]

    @RULE(
        "security_field opt_security_fields",
        "empty",
    )
    def p_opt_security_fields(self, p) -> dict[str, Tx]:
        p[0] = {} if len(p) == 2 else p[1] | p[2]
        return p[0]

    @RULE(
        "'<' ENTRYPOINT '>'",
        "empty",
    )
    def p_opt_entrypoint(self, p) -> bool:
        p[0] = len(p) > 2
        return p[0]

    # SECURITY SECTION
    ####################################################################

    ####################################################################
    # COMMON RULES
    @RULE(
        "DATA",
        "DETAILS",
        "DNC",
        "DNCDIR",
        "ID",
        "RESTYPE",
        "VALUE",
    )
    def p_valid_field_id(self, p) -> str:
        p[0] = p[1]
        return p[0]

    @RULE(
        "field_mod opt_field_mods",
        "empty",
    )
    def p_opt_field_mods(self, p) -> tuple[bool, bool, bool, bool]:
        p[0] = [False, False, False, False]
        if len(p) == 3:
            p[0] = list(p[2])
            p[0][p[1]] = True
        return tuple(p[0])

    @RULE(
        "HIDDEN",
        "OPTIONAL",
        "READONLY",
    )
    def p_field_mod(self, p) -> int:
        kws = ["hidden", "optional", "readonly"]
        p[0] = kws.index(p[1])
        return p[0]

    @RULE(
        "':' VALUE opt_properties opt_pipeline",
        "':' SELVES opt_pipeline",
    )
    def p_opt_constraint(self, p) -> Tx:
        if len(p) == 5:
            p[0] = Tx([Ref(["value"] + p[3])] + p[4])
        else:
            p[0] = Tx([Ref(["selves"])] + p[3])
        return p[0]

    @RULE(
        # Normal functions
        "ID '(' ')'",  # 4
        "ID '.' ID '(' ')'",  # 6
        "ID '(' arg opt_args ')'",  # 6
        "ID '.' ID '(' arg opt_args ')'",  # 8
        # Mapped functions
        "ID '[' ID opt_params ']' '(' ID opt_properties opt_pipeline ')'",  # 11
        "ID '.' ID '[' ID opt_params ']' '(' ID opt_properties opt_pipeline ')'",  # 13
        "ID '[' ID opt_params ']' '(' SELVES opt_pipeline ')'",  # 10
        "ID '.' ID '[' ID opt_params ']' '(' SELVES opt_pipeline ')'",  # 12
    )
    def p_func(self, p) -> Func | MappedFunc:
        match (len(p), p[2], p[4] if len(p) > 4 else None):
            case (4, _, _):
                p[0] = Func(p[1], "", [])
            case (6, ".", "("):
                p[0] = Func(p[3], p[1], [])
            case (6, _, _):
                p[0] = Func(p[1], "", [p[3]] + p[4])
            case (8, ".", _):
                p[0] = Func(p[3], p[1], [p[5]] + p[6])
            case (_, "[", _):
                p[0] = MappedFunc(
                    p[1],
                    "",
                    [p[3]] + p[4],
                    Tx([Ref([p[7]] + p[8])] + p[9]),
                )

            case (_, ".", "["):
                p[0] = MappedFunc(
                    p[3],
                    p[1],
                    [p[5]] + p[6],
                    Tx([Ref([p[9]] + p[10])] + p[11]),
                )

        return p[0]

    @RULE(
        # Normal functions
        "PIPEOP func opt_pipeline",  # Other
        "empty",
    )
    def p_opt_pipeline(self, p) -> list[Func | MappedFunc]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "',' ID opt_params",
        "empty",
    )
    def p_opt_params(self, p) -> list[str]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "INT",
        "INT '.' INT",
        "STR",
        "VALUE opt_pipeline",
        "SELVES opt_pipeline",
        "ID opt_properties opt_pipeline",
        "SELF opt_properties opt_pipeline",
    )
    def p_arg(self, p) -> Int | Float | Str | Ref | Tx:
        if len(p) == 3 and p[1] == "value":
            p[0] = Tx([Ref(["value"])] + p[2])
        elif len(p) == 3 and p[1] == "selves":
            p[0] = Tx([Ref(["selves"])] + p[2])
        elif len(p) == 4 and p[2] == ".":
            p[0] = Float(float(f"{p[1]}.{p[3]}"))
        elif len(p) == 4 and p[3] == []:
            p[0] = Ref([p[1]] + p[2])
        elif len(p) == 4:
            p[0] = Tx([Ref([p[1]] + p[2])] + p[3])
        elif isinstance(p[1], int):
            p[0] = Int(p[1])
        else:
            p[0] = Str(p[1])
        return p[0]

    @RULE(
        "',' arg opt_args",
        "empty",
    )
    def p_opt_args(self, p) -> list[Int | Float | Str | Ref]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "'.' ID opt_properties",
        "'.' VALUE opt_properties",
        "empty",
    )
    def p_opt_properties(self, p) -> list[str]:
        p[0] = [] if len(p) == 2 else [p[2]] + p[3]
        return p[0]

    @RULE(
        "INT",
        "INT '.' INT",
        "STR",
        "BOOLEAN",
        "SELVES",
        "VALUE opt_properties",
        "SELF opt_properties",
        "ID opt_properties",
        "effect_func",
    )
    def p_expr(
        self, p
    ) -> Float | Ref | Boolean | Int | Ref | Func | MappedFunc | Str:
        if len(p) == 2 and p[1] == "selves":
            p[0] = Ref(["selves"])
        elif len(p) == 4 and p[2] == ".":
            p[0] = Float(float(f"{p[1]}.{p[3]}"))
        elif len(p) == 3:
            p[0] = Ref([p[1]] + p[2])
        elif isinstance(p[1], bool):
            p[0] = Boolean(p[1])
        elif isinstance(p[1], int):
            p[0] = Int(p[1])
        elif isinstance(p[1], Func) or isinstance(p[1], MappedFunc):
            p[0] = p[1]
        else:
            p[0] = Str(p[1])
        return p[0]

    # COMMON RULES
    ####################################################################
