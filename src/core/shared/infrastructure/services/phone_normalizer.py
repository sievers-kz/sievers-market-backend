import phonenumbers
from phonenumbers import PhoneNumberFormat


class PhoneNormalizer:
    def __init__(self, default_region: str = "KZ"):
        self.default_region = default_region

    def normalize(self, phone_str: str):
        try:
            parsed = phonenumbers.parse(phone_str, self.default_region)
            if not phonenumbers.is_valid_number_for_region(parsed, self.default_region):
                raise ValueError("Invalid phone number format")

            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException as exc:
            raise ValueError(str(exc)) from exc
