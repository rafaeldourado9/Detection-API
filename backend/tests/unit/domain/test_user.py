import pytest

from src.domain.user.entities import User
from src.domain.user.value_objects import Email, HashedPassword


class TestEmail:
    def test_valid_email(self) -> None:
        email = Email("user@example.com")
        assert email.value == "user@example.com"

    def test_invalid_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            Email("not-an-email")

    def test_empty_email_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid email"):
            Email("")


class TestHashedPassword:
    def test_valid_hash(self) -> None:
        hp = HashedPassword("$2b$12$somehash")
        assert hp.value == "$2b$12$somehash"

    def test_empty_hash_raises(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            HashedPassword("")


class TestUser:
    def test_create_user(self) -> None:
        user = User.create(email="a@b.com", hashed_password="hashed123")
        assert user.email.value == "a@b.com"
        assert user.is_active is True
        assert user.id is not None

    def test_user_is_active_by_default(self) -> None:
        user = User.create(email="x@y.com", hashed_password="h")
        assert user.is_active is True
