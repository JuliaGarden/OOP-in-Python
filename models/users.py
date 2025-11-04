from typing import Dict
from typing import List
from exceptions import InvalidEmailError

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str):
        if "@" not in email:
            raise InvalidEmailError("Email должен содержать '@'")
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = hash(password)
        self.is_active = True

    def get_profile(self) -> Dict[str, object]:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }

    def update_profile(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def deactivate(self) -> None:
        self.is_active = False


class Admin(User):
    def __init__(self, user_id: int, username: str, email: str, password: str):
        super().__init__(user_id, username, email, password)

    def ban_user(self, user_id: int) -> bool:
        print(f"User {user_id} is banned")
        return True

    def view_all_users(self, all_users: List[User]) -> List[User]:
        return [user for user in all_users if user.user_id != self.user_id]



