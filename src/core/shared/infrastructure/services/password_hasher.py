import bcrypt


class BcryptPasswordHasher:

    @staticmethod
    def hash_password(password_str: str):
        hashed = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed: str):
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))