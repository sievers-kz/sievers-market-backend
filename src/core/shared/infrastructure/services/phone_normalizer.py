import phonenumbers
from phonenumbers import PhoneNumberFormat

from src.core.shared.infrastructure.exceptions.exception_classes import PhoneNormalizerServiceError


class PhoneNormalizer:
    @staticmethod
    def normalize(phone_str: str):
        try:
            parsed = phonenumbers.parse(phone_str, "KZ")
            if not phonenumbers.is_valid_number_for_region(parsed, "KZ"):
                raise PhoneNormalizerServiceError(
                    code="number_parse_error",
                    context={"operation": "phone_normalize"}
                )
            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException as exc:
            raise PhoneNormalizerServiceError(
                code="unexpected_number_parse_error",
                context={"operation": "phone_normalize"}
                ) from exc
