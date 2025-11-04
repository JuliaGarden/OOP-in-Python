from datetime import datetime

class Subscription:
    def __init__(self, sub_id: int, customer_id: int, plan_name: str, start_date: str, end_date: str):
        self.sub_id = sub_id
        self.customer_id = customer_id
        self.plan_name = plan_name
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True

    def is_expired(self) -> bool:
        try:
            end = datetime.strptime(self.end_date, "%Y-%m-%d")
            return datetime.now() > end
        except ValueError:
            #если дата в неверная, то подписка недействительна
            return True