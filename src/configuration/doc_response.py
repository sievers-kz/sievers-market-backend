from src.core.shared.domain.exceptions import DomainException


def doc_responses(*exceptions: type[DomainException] | tuple | list) -> dict:
    result: dict[int, dict] = {}

    flat_exceptions = []
    for exc in exceptions:
        if isinstance(exc, (tuple, list)):
            flat_exceptions.extend(exc)
        else:
            flat_exceptions.append(exc)

    for exc in flat_exceptions:
        code = exc.status_code
        result.setdefault(code, {"description": "", "content": {"application/json": {"examples": {}}}})
        result[code]["content"]["application/json"]["examples"][exc.__name__] = {
            "summary": exc.message,
            "value": {"error_code": exc.error_code, "message": exc.message},
        }

    return result
