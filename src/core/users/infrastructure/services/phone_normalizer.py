import phonenumbers
from phonenumbers import PhoneNumberFormat


class PhoneNormalizer:
    @staticmethod
    def normalize(phone_str: str):
        try:
            parsed = phonenumbers.parse(phone_str, "KZ")
            if not phonenumbers.is_valid_number_for_region(parsed, "KZ"):
                raise ValueError("Недопустимый формат номера телефона!")
            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException as e:
            raise ValueError(f"Ошибка при обработке номера телефона: {e}")