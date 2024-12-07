from .base import CompiledResource, CompiledResourceField, Effects, Rules


class Database(CompiledResource):
    @property
    def name(self) -> str:
        return "Database"

    @property
    def archetype(self) -> str:
        return "description"

    @property
    def data(self) -> list:
        return [CompiledResourceField("cx_env_var")]

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
        return []


includes = []
resources = [Database]
datatypes = {}
functions = {}
