from abc import ABC, abstractmethod

import phonenumbers
from phonenumbers import PhoneNumberFormat


class AbstractPhoneNormalizer(ABC):
    @abstractmethod
    def normalize(self, phone_str: str):
        raise NotImplementedError


class PhoneNormalizer(AbstractPhoneNormalizer):
    def normalize(self, phone_str: str):
        try:
            parsed = phonenumbers.parse(phone_str, "KZ")
            if not phonenumbers.is_valid_number_for_region(parsed, "KZ"):
                raise ValueError("Invalid phone number format")

            return phonenumbers.format_number(parsed, PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException as exc:
            raise ValueError(str(exc)) from exc
