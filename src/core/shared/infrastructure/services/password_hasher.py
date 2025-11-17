from abc import ABC, abstractmethod

import bcrypt


class AbstractPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password_str: str):
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, password: str, hashed: str):
        raise NotImplementedError


class BcryptPasswordHasher(AbstractPasswordHasher):

    def hash_password(self, password_str: str):
        hashed = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def verify_password(self, password: str, hashed: str):
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))