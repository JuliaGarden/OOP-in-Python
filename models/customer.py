from typing import List, Optional
from .users import User
from .subscription import Subscription
from .viewing_history import ViewingHistory

class Customer(User):
    def __init__(self, user_id: int, username: str, email: str, password: str, phone: str):
        super().__init__(user_id, username, email, password)
        self.phone = phone
        self.subscription: Optional[Subscription] = None
        self.viewing_history: List[ViewingHistory] = []

    def get_subscription(self) -> Optional[Subscription]:
        return self.subscription

    def add_viewing_history(self, viewing: ViewingHistory) -> None:
        self.viewing_history.append(viewing)

    def is_premium(self) -> bool:
        return self.subscription is not None and self.subscription.plan_name == "Premium"

    def is_subscription_active(self) -> bool:
        if self.subscription is None:
            return False
        return not self.subscription.is_expired()