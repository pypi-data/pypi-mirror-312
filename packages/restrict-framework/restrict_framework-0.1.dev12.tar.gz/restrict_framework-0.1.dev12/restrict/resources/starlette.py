from .base import CompiledResource, Effects, Rules


class Authentication(CompiledResource):
    @property
    def name(self) -> str:
        return "Authentication"

    @property
    def archetype(self) -> str:
        return "moment"

    @property
    def data(self) -> list:
        return []

    @property
    def dnc(self) -> list:
        return []

    @property
    def effects(self) -> Effects:
        return Effects()

    @property
    def security(self) -> Rules:
        return Rules()

    @property
    def globals(self) -> list[str]:
        return ["actor"]


includes = []
resources = [Authentication]
datatypes = {}
functions = {}
