from typing import List
from exceptions import *
from .users import User
from .content import Content

class StreamingService:
    def __init__(self):
        self.users: List[User] = []
        self.contents: List[Content] = []

    def add_user(self, user: User) -> None:
        if any(u.user_id == user.user_id for u in self.users):
            raise UserAlreadyExistsError(f"User with ID {user.user_id} already exists")
        self.users.append(user)

    def get_user(self, user_id: int) -> User:
        for user in self.users:
            if user.user_id == user_id:
                return user
        raise UserNotFoundError(f"User with ID {user_id} not found")

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        self.users.remove(user)
        return True

    def add_content(self, content: Content) -> None:
        self.contents.append(content)

    def get_content(self, content_id: int) -> Content:
        for content in self.contents:
            if content.content_id == content_id:
                return content
        raise ContentNotFoundError(f"Content with ID {content_id} not found")

    def update_user(self, user_id: int, **kwargs) -> bool:
        user = self.get_user(user_id)
        user.update_profile(**kwargs)
        return True

    def delete_content(self, content_id: int) -> bool:
        content = self.get_content(content_id)
        self.contents.remove(content)
        return True

    def watch_content(self, user_id: int, content_id: int) -> str:
        # Сначала проверяем существование контента
        content = self.get_content(content_id)  # ← может выбросить ContentNotFoundError
        # Потом проверяем подписку
        user = self.get_user(user_id)
        if hasattr(user, 'is_subscription_active') and not user.is_subscription_active():
            raise SubscriptionExpiredError("Ваша подписка истекла...")
        return f"Просмотр: {content.title}"