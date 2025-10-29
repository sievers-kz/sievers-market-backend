# import logging
#
# from fastapi import Request, status
# from fastapi.exceptions import RequestValidationError
# from starlette.responses import JSONResponse
#
# from src.api.shared.exceptions.error_messages import APPLICATION_HTTP_STATUS_MAP, get_unified_error_message
# from src.core.shared.application.exceptions.base_exception import BaseApplicationError
#
#
# async def application_exception_handler(request: Request, exc: BaseApplicationError):
#     logging.error(f"{exc.__class__.__name__}: {exc.meta.code}", extra=exc.to_internal())
#
#     status_code = APPLICATION_HTTP_STATUS_MAP.get(type(exc), 500)
#     message = get_unified_error_message(exc.meta.code, exc.meta.context.get("verbose_name"))
#
#     client_msg = exc.to_client()
#     return JSONResponse(
#         status_code=status_code,
#         content={
#             "error": {
#                 **client_msg,
#                 "message": message
#             }
#         }
#     )
#
#
# async def pydantic_exception_handler(request: Request, exc: RequestValidationError):
#     """Обработчик Pydantic ValidationError"""
#
#     errors = exc.errors()
#     first_error = errors[0]
#
#     # 1. Базовая информация об ошибке
#     error_type = first_error["type"]  # "missing", "string_type", etc.
#     loc = first_error["loc"]
#     field_name = loc[-1] if loc else None
#
#     # 2. Достаем DTO модель из FastAPI route
#     verbose_name = field_name  # fallback - английское название
#
#     try:
#         # FastAPI хранит body_field в route
#         body_field = request.scope['route'].body_field
#
#         if body_field and hasattr(body_field.type_, 'model_json_schema'):
#             # Получаем JSON схему DTO (Pydantic v2)
#             schema = body_field.type_.model_json_schema()
#
#             # Ищем наше поле в properties
#             field_schema = schema.get('properties', {}).get(field_name)
#
#             # Достаем title (наш verbose_name)
#             if field_schema and field_schema.get('title'):
#                 verbose_name = field_schema['title']
#
#     except (KeyError, AttributeError) as e:
#         # Если что-то пошло не так - используем английское название
#         logging.warning(f"Could not extract verbose_name for field {field_name}: {e}")
#
#     # 3. Формируем сообщение
#     message = get_unified_error_message(error_type, verbose_name)
#
#     # 4. Логируем
#     logging.info(
#         f"Pydantic validation error: {error_type}",
#         extra={"field": field_name, "error_type": error_type}
#     )
#
#     # 5. Возвращаем JSON
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "error": {
#                 "code": error_type,
#                 "field": field_name,
#                 "message": message
#             }
#         }
#     )