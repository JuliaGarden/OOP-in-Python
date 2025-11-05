import json
import os
from typing import Dict, Any

def save_to_json(data: Dict[str, Any], filename: str) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка записи в JSON: {e}")

def load_from_json(filename: str) -> Dict[str, Any]:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Возвращён пустой словарь.")
        return {"users": [], "content": []}
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON: {e}")
        return {"users": [], "content": []}