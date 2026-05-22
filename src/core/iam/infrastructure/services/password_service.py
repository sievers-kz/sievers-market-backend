from passlib.context import CryptContext
from rbloom import Bloom


class PasswordService:
    def __init__(self, bloom: Bloom):
        self._bloom = bloom
        self._ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def validate(self, raw: str) -> None:
        if len(raw) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        if len(raw) > 64:
            raise ValueError("Пароль не должен превышать 64 символа")
        if raw in self._bloom:
            raise ValueError("Пароль слишком распространен. Придумайте другой")

    def hash(self, raw: str) -> str:
        return self._ctx.hash(raw)

    def verify(self, raw: str, hashed: str) -> bool:
        return self._ctx.verify(raw, hashed)

