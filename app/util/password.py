from passlib.context import CryptContext
from secrets import choice
from string import ascii_letters, digits, punctuation


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return context.verify(password, hashed)


def is_password_hashed(password: str) -> bool:
    return context.identify(password) is not None


def generate_password(length: int = 12) -> str:
    choices = ascii_letters + digits + punctuation
    return "".join(choice(choices) for _ in range(length))