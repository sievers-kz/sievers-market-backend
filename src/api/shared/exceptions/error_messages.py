from src.api.auth.exceptions.error_messages import AUTH_ERROR_MESSAGES, AUTH_HTTP_STATUS_MAP
from src.api.users.exceptions.error_messages import USER_ERROR_MESSAGES, USER_HTTP_STATUS_MAP, PYDANTIC_ERROR_MESSAGES

APPLICATION_ERROR_MESSAGES = {
    **USER_ERROR_MESSAGES,
    **AUTH_ERROR_MESSAGES,
    **PYDANTIC_ERROR_MESSAGES
}


APPLICATION_HTTP_STATUS_MAP = {
    **USER_HTTP_STATUS_MAP,
    **AUTH_HTTP_STATUS_MAP
}


def get_unified_error_message(code: str, verbose_name: str) -> str:
    template = APPLICATION_ERROR_MESSAGES.get(code, "Произошла ошибка")

    if verbose_name and "{verbose_name}" in template:
        return template.format(verbose_name=verbose_name)

    return template
