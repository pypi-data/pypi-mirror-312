from dataclasses import dataclass
from pathlib import Path
from ..ply.lex import lex, TOKEN


@dataclass(frozen=True)
class RestrictLexerError:
    value: str
    lineno: int
    pos: int


class RestrictLexer:
    tokens = [
        "ACCESSORS",
        "BOOLEAN",
        "COMPUTED",
        "CREATE",
        "DATA",
        "DELETE",
        "DESCTYPE",
        "DETAILS",
        "DNC",
        "DNCDIR",
        "EFFECTS",
        "ENTRYPOINT",
        "HIDDEN",
        "ID",
        "INT",
        "LIST",
        "MODIFY",
        "MUTATORS",
        "OPTIONAL",
        "OVERRIDE",
        "PATH",
        "PIPEOP",
        "READONLY",
        "RESNAME",
        "RESTYPE",
        "SECURITY",
        "SELF",
        "SELVES",
        "SET",
        "STR",
        "USE",
        "VALUE",
    ]
    literals = "{}<>()|:,.*[];"
    states = [
        ("use", "exclusive"),
        ("refer", "exclusive"),
        ("refpath", "exclusive"),
    ]

    t_PIPEOP = r"\|>"

    t_ignore = " "
    t_use_ignore = " "
    t_refer_ignore = " "
    t_refpath_ignore = ""

    @TOKEN(r"\n+")
    def t_newline(self, t):
        t.lexer.lineno += len(t.value)

    @TOKEN(r"\buse\b")
    def t_USE(self, t):
        t.lexer.push_state("use")
        return t

    @TOKEN(r"\brefer\b")
    def t_REFER(self, t):
        t.lexer.push_state("refer")
        t.type = "USE"
        return t

    @TOKEN(r"\b(to|as)\b")
    def t_refer_CONJ(self, _):
        pass

    @TOKEN(r"\b[a-z][a-z_0-9]*\b")
    def t_refer_ID(self, t):
        t.lexer.pop_state()
        return t

    @TOKEN("<")
    def t_refer_use_LT(self, t):
        t.lexer.push_state("refpath")

    @TOKEN(r"[a-z/\\]+")
    def t_refpath_PATH(self, t):
        t.value = Path(t.value)
        t.lexer.pop_state()
        return t

    @TOKEN(r">")
    def t_refer_GT(self, _):
        pass

    @TOKEN(r">")
    def t_use_GT(self, t):
        t.lexer.pop_state()

    @TOKEN(r"\b(true|false)\b")
    def t_BOOLEAN(self, t):
        t.value = t.value == "true"
        return t

    @TOKEN(r"\b(party|role|thing|interval|moment|place)\b")
    def t_RESTYPE(self, t):
        return t

    @TOKEN(r"\b(next|previous|root)\b")
    def t_DNCDIR(self, t):
        return t

    @TOKEN(r"\bdescription\b")
    def t_DESCTYPE(self, t):
        return t

    @TOKEN(
        r"\b("
        "data|dnc|effects|security|"
        "computed|readonly|hidden|optional|"
        "override|"
        "list|set|"
        "create|modify|delete|"
        "self|selves|"
        "mutators|accessors|"
        "entrypoint|"
        "details|"
        "value"
        r")\b"
    )
    def t_uppers(self, t):
        t.type = t.value.upper()
        return t

    @TOKEN(r"\b([a-z][a-z_0-9]*|_)\b")
    def t_ID(self, t):
        return t

    @TOKEN(r"\b[A-Z][a-zA-Z0-9]*\b")
    def t_RESNAME(self, t):
        return t

    @TOKEN(r"\b[0-9]+\b")
    def t_INT(self, t):
        t.value = int(t.value)
        return t

    @TOKEN(r'"(?:[^"\\]|\\.)*"')
    def t_STR(self, t):
        t.value = t.value[1:-1]
        return t

    def __init__(self):
        self._errors = []
        self._lexer = None

    def t_refpath_error(self, t):
        self._errors.append(
            RestrictLexerError(t.value, t.lexer.lineno, t.lexpos)
        )
        t.lexer.skip(1)

    def t_refer_error(self, t):
        self._errors.append(
            RestrictLexerError(t.value, t.lexer.lineno, t.lexpos)
        )
        t.lexer.skip(1)

    def t_use_error(self, t):
        self._errors.append(
            RestrictLexerError(t.value, t.lexer.lineno, t.lexpos)
        )
        t.lexer.skip(1)

    def t_error(self, t):
        self._errors.append(
            RestrictLexerError(t.value, t.lexer.lineno, t.lexpos)
        )
        t.lexer.skip(1)

    def build(self, **kwargs):
        self._lexer = lex(module=self, **kwargs)
        return self

    def clone(self):
        if self._lexer is None:
            raise RuntimeError("Cannot clone an unbuilt RestrictLexer")
        lexer = RestrictLexer()
        lexer._lexer = self._lexer.clone()
        return lexer

    def input(self, input):
        if self._lexer is None:
            raise RuntimeError(
                "Cannot set the input of an unbuilt RestrictLexer"
            )
        self._lexer.lineno = 1
        while self._lexer.current_state() != "INITIAL":
            self._lexer.pop_state()
        self._errors = []
        self._lexer.input(input)

    @property
    def errors(self):
        return [x for x in self._errors]

    def token(self):
        if self._lexer is None:
            raise RuntimeError("Cannot use an unbuilt RestrictLexer")
        return self._lexer.token()

    @property
    def lineno(self):
        if self._lexer is None:
            return -1
        return self._lexer.lineno

    @property
    def lexpos(self):
        if self._lexer is None:
            return -1
        return self._lexer.lexpos

    def __iter__(self):
        if self._lexer is None:
            raise RuntimeError("Cannot use an unbuilt RestrictLexer")
        return self._lexer.__iter__()
