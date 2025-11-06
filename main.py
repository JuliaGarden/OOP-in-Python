from models.service import StreamingService
from models import Customer, Subscription, ViewingHistory, Content
from exceptions import *
from storage.json_serealization import save_to_json, load_from_json
from storage.xml_serealization import save_to_xml, load_from_xml

cinema = StreamingService()

print("Добавление пользователей")
user_Krista = Customer(1, "Krista", "KrisImy@example.com", "123", "+123")
user_Alice = Customer(456, "Alice", "DaGirl@example.com", "456", "+456")
cinema.add_user(user_Krista) #Добавляем пользователей в систему
cinema.add_user(user_Alice)

#Назначение подписки и истории просмотра
user_Krista.subscription = Subscription(
    sub_id = 2,
    customer_id = 1,
    plan_name="Premium",
    start_date="2025-01-01",
    end_date="2026-12-31"
)
user_Alice.add_viewing_history(
    ViewingHistory(
        history_id = 1,
        customer_id = 456,
        content_id = 101,
        watched_at = "2025-11-05",
        progress = 0.8,
        duration_watched = 4500
    )
)

print("Список всех пользователей:")
for user in cinema.users:
    profile = user.get_profile()
    sub = user.get_subscription()
    print(f"ID: {profile['user_id']}, имя: {profile['username']}, email: {profile['email']}")
    if sub:
        print(f"Подписка: {sub.plan_name} (активна до {sub.end_date})")
    else:
        print("Подписка: нет")



#Проверка исключений
print("\n\nТест 1: Попытка посмотреть несуществующий контент")
try:
    cinema.watch_content(1, 999)  #контент с ID=999 не существует
except ContentNotFoundError as e:
    print(f"Поймано исключение: {e}")
except SubscriptionExpiredError as e:
    print(f"Ошибка подписки (неожиданно): {e}")

print("\nТест 2: Попытка создать пользователя с некорректным email")
try:
    bad_user = Customer(999, "BadUser", "invalid-email", "123", "+000")
except InvalidEmailError as e:
    print(f"Поймано исключение InvalidEmailError: {e}")

print("\nТест 3: Попытка получить несуществующего пользователя")
try:
    cinema.get_user(9999)   #такого ID нет
except UserNotFoundError as e:
    print(f"Поймано исключение UserNotFoundError: {e}")

print("\nТест 4: Попытка добавить пользователя с уже существующим ID")
try:
    duplicate_user = Customer(1, "Duplicate", "dup@example.com", "123", "+111")
    cinema.add_user(duplicate_user)  # ID=1 уже есть у Krista
except UserAlreadyExistsError as e:
    print(f"Поймано исключение UserAlreadyExistsError: {e}")

print("\nТест 5: Успешный просмотр с активной подпиской")
#Добавляем контент
movie = Content(1, "Bad Influence", "A playboy who shows a white collar guy some thrills", 1990, 109)
cinema.add_content(movie)
# Восстанавливаем активную подписку
user_Krista.subscription = Subscription(
    sub_id = 2,
    customer_id = 1,
    plan_name = "Premium",
    start_date = "2025-01-01",
    end_date = "2026-12-31"
)
try:
    result = cinema.watch_content(1, 1)
    print(f"{result}")
except Exception as e:
    print(f"Ошибка: {e}")



#Тесты CRUD
print("\n\nТесты CRUD")
print("Тест 6: Обновление профиля пользователя")
cinema.update_user(1, phone="+73829301832")
print(f"Новый телефон Krista: {user_Krista.phone}")

print("\nТест 7: Удаление контента")
cinema.delete_content(1)
try:
    cinema.get_content(1)
except ContentNotFoundError as e:
    print(f"Контент успешно удалён: {e}")

# Добавление фильма и сериала
print("\nТест 8:Добавление контента: фильм и сериал")
cinema.add_content(Content(1, "Bad Influence", "A playboy who shows a white collar guy some thrills", 1990, 109))
cinema.add_content(Content(2, "Inception", "Dream thief steals secrets", 2010, 148))
cinema.add_content(Content(3, "Breaking Bad", "Chemistry teacher turns criminal", 2008, 49))
print("Список контента:")
for item in cinema.contents:
    print(f"ID: {item.content_id}, название: {item.title}, описание: {item.description}")


#данные в xml json
sample_data = {
    "users": [
        {
            "user_id": 47,
            "username": "George",
            "email": "Harrison@g.c",
            "is_active": True,
            "role": "customer",
            "phone": "+123456789",
            "subscription": {
                "sub_id": 47,
                "plan_name": "Premium",
                "start_date": "2025-01-01",
                "end_date": "2025-12-31"
            }
        }
    ],
    "content" : [
        {
          "content_id": 1,
          "title": "The man who fell to earth",
          "description": "An alien must pose as a human to save his dying planet",
          "release_year": 1976,
          "duration": 148,
          "type": "movie",
          "is_premiere": False
        },
        {
            "content_id": 2,
            "title": "The long walk",
            "description": "Fifty boys in an annually televised competitive walking marathon",
            "release_year": 2025,
            "duration": 108,
            "type": "movie",
            "is_premiere": True
        }
    ]
}

print("\n\nТест 9:")
save_to_json(sample_data, "data/cinema_data.json")
save_to_xml(sample_data, "data/cinema_data.xml")
loaded_json = load_from_json("data/cinema_data.json")
loaded_xml = load_from_xml("data/cinema_data.xml")
print("JSON загружен, пользователей:", len(loaded_json["users"]))
print("XML загружен, контента:", len(loaded_xml["content"]))

print("\nТест 10: Загрузка из JSON и XML")
# Загрузка из JSON
print("Пользователи из JSON")
data_json = load_from_json("data/cinema_data.json")
for user in data_json.get("users", []):
    print(f"ID: {user['user_id']}, Имя: {user['username']}, Email: {user['email']}")
# Загрузка из XML
print("\nПользователи из XML")
data_xml = load_from_xml("data/cinema_users.xml")
for user in data_xml.get("users", []):
    print(f"ID: {user['user_id']}, Имя: {user['username']}, Email: {user['email']}")

