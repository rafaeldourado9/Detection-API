from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str


@dataclass(frozen=True)
class LoginCommand:
    email: str
    password: str
