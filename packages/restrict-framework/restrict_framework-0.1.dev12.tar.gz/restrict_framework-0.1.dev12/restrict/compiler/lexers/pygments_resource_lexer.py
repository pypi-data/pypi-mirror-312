from pygments.lexer import RegexLexer, bygroups
from pygments.token import (
    Keyword,
    Comment,
    Operator,
    Name,
    Punctuation,
    Whitespace,
)

__all__ = ["ResourceLexer"]


class ResourceLexer(RegexLexer):
    name = "Restrict Framework Resource Language"
    aliases = ["restrict-resources", "restrict-resource"]
    filenames = ["*.resources", "*.resource"]
    mimetypes = ["text/x-restrict-resource"]

    tokens = {
        "root": [
            (
                r"^\s*(versioned\s+)?(override|party|role|moment|interval|description)",
                Keyword.Declaration,
            ),
            (r"refer to <[^>]+> as [a-z]*", Comment.PreprocFile),
            (r"use <[^>]+>", Comment.PreprocFile),
            (r"(optional|page|readonly|hidden)", Keyword.Declaration),
            (
                r"\b(accessors|mutators|dnc|access|defined|security|effects|as)\b",
                Keyword.Reserved,
            ),
            (r"\b(in|is)\b", Operator.Word),
            (r"<(party|next|previous|role):(\d+|\*)>", Name.Decorator),
            (r"<entrypoint|description>", Name.Decorator),
            (r"\b[A-Z][a-zA-Z]+(\(\s*(\d+|\d+\s*,\s*\d+)\s*\))?", Name.Class),
            (
                r"\b([a-z][_a-zA-Z]+)\s*(:)",
                bygroups(Name.Property, Punctuation),
            ),
            (r"\b([a-z][_a-zA-Z]+)\b", Name.Property),
            (r"(<|>|=|\||\*)", Operator),
            (r"\s+", Whitespace),
            (r"\b[a-z]+\b", Name.Variable),
            (r"\/", Punctuation),
            (r"\{", Punctuation),
            (r"\}", Punctuation),
            (r"\.", Punctuation),
            (r"\[", Punctuation),
            (r"\]", Punctuation),
            (r"\(", Punctuation),
            (r"\)", Punctuation),
            (":", Punctuation),
            (",", Punctuation),
        ],
    }
