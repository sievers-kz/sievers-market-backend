import bcrypt


class BcryptPasswordHasher:

    @staticmethod
    def hash_password(password_str: str):
        hashed = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")


