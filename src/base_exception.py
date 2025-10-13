from dataclasses import dataclass, field as dict_field


@dataclass(frozen=True)
class ErrorMeta:
    code: str
    details: str | None = None
    context: dict = dict_field(default_factory=dict)
    _allowed_client_keys = frozenset(["field", "verbose_name"])

    def to_client(self):
        data = {"code": self.code}

        for key in self._allowed_client_keys:
            if key in self.context:
                data[key] = self.context[key]

        return data

    def to_internal(self):
        return {
            "code": self.code,
            "details": self.details,
            "context": self.context
        }


class BaseApplicationError(Exception):
    def __init__(self, *, code: str, details: str | None = None, context: dict | None = None):
        self.meta = ErrorMeta(code=code, details=details, context=context or {})
        super().__init__(f"{self.__class__.__name__}({code})")

    def to_client(self) -> dict:
        return self.meta.to_client()

    def to_internal(self) -> dict:
        return self.meta.to_internal()
