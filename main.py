from models.service import StreamingService
from models import *
from exceptions import *
from storage.json_serealization import save_to_json, load_from_json
from storage.xml_serealization import save_to_xml, load_from_xml

service = StreamingService()
user_Krista = Customer(1, "Krista", "KrisImy@example.com", "123", "+123")
service.add_user(user_Krista)

print("Тест 1: Попытка посмотреть несуществующий контент")
try:
    service.watch_content(1, 999)
except ContentNotFoundError as e:
    print(f"Поймано исключение ContentNotFoundError: {e}")
except SubscriptionExpiredError as e:
    print(f"Подписка неактивна, но контент тоже не найден: {e}")


print("\nТест 2: Попытка посмотреть с просроченной подпиской")
#Назначаем просроченную подписку
expired_sub = Subscription(
    sub_id = 1,
    customer_id = 1,
    plan_name = "Premium",
    start_date = "2023-01-01",
    end_date = "2023-12-31"
)
user_Krista.subscription = expired_sub
try:
    service.watch_content(1, 1)
except SubscriptionExpiredError as e:
    print(f"Поймано исключение SubscriptionExpiredError: {e}")
except ContentNotFoundError as e:
    print(f"Контент не найден: {e}")


print("\nТест 3: Добавим контент и проверим успешный просмотр")
from models.content import Content
content = Content(1, "Bad Influence", "A playboy who shows a white collar guy some thrills", 1990, 109)
service.add_content(content)
#Назначим активную подписку
active_sub = Subscription(
    sub_id = 2,
    customer_id = 1,
    plan_name = "Premium",
    start_date = "2025-01-01",
    end_date = "2026-12-31"
)
user_Krista.subscription = active_sub
try:
    result = service.watch_content(1, 1)
    print(f"Успешный просмотр: {result}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")


sample_data = {
    "users": [
        {
            "user_id": 1,
            "username": "George",
            "email": "Harrison@g.c",
            "is_active": True,
            "role": "customer",
            "phone": "+123456789",
            "subscription": {
                "sub_id": 1,
                "plan_name": "Premium",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31"
            }
        }
    ],
    "content": [
        {
            "content_id": 1,
            "title": "Inception",
            "description": "A thief who steals corporate secrets...",
            "release_year": 2010,
            "duration": 148,
            "type": "movie",
            "is_premiere": False
        }
    ]
}

print("\nТест 4: Обновление профиля")
service.update_user(1, phone="+73829301832")
print("Новый телефон:", user_Krista.phone)

print("\nТест 5: Удаление контента")
service.delete_content(1)
try:
    service.get_content(1)
except ContentNotFoundError as e:
    print("Контент удалён:", e)

print("\nТест 6:")
save_to_json(sample_data, "data/cinema_data.json")
save_to_xml(sample_data, "data/cinema_data.xml")
loaded_json = load_from_json("data/cinema_data.json")
loaded_xml = load_from_xml("data/cinema_data.xml")
print("JSON загружен, пользователей:", len(loaded_json["users"]))
print("XML загружен, контента:", len(loaded_xml["content"]))