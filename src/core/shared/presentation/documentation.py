from dataclasses import dataclass
from inspect import cleandoc

from src.configuration.doc_response import doc_responses


@dataclass(frozen=True, slots=True)
class RouteDocs:
    operation_id: str
    summary: str
    description: str
    responses: tuple[type[Exception], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "description", cleandoc(self.description))

    @property
    def responses_doc(self) -> dict:
        return doc_responses(self.responses)
