import xml.etree.ElementTree as ET
from typing import Dict, Any
import os

def save_to_xml(data: Dict[str, Any], filename: str) -> None:
    root = ET.Element("cinema")

    users_elem = ET.SubElement(root, "users")
    for user in data.get("users", []):
        user_elem = ET.SubElement(
            users_elem, "user",
            user_id=str(user["user_id"]),
            username=user["username"],
            email=user["email"],
            is_active=str(user["is_active"]).lower(),
            role=user["role"]
        )
        if user["role"] == "customer":
            ET.SubElement(user_elem, "phone").text = user.get("phone", "")
            if user.get("subscription"):
                sub = user["subscription"]
                ET.SubElement(
                    user_elem, "subscription",
                    sub_id=str(sub["sub_id"]),
                    plan_name=sub["plan_name"],
                    start_date=sub["start_date"],
                    end_date=sub["end_date"]
                )

    # Контент
    content_elem = ET.SubElement(root, "content")
    for item in data.get("content", []):
        if item["type"] == "movie":
            elem = ET.SubElement(
                content_elem, "movie",
                content_id=str(item["content_id"]),
                title=item["title"],
                release_year=str(item["release_year"]),
                duration=str(item["duration"]),
                is_premiere=str(item["is_premiere"]).lower()
            )
        else:
            elem = ET.SubElement(
                content_elem, "series",
                content_id=str(item["content_id"]),
                title=item["title"],
                release_year=str(item["release_year"]),
                duration=str(item["duration"]),
                seasons=str(item["seasons"])
            )
        ET.SubElement(elem, "description").text = item["description"]

    #Запись в файл
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    tree = ET.ElementTree(root)
    try:
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка записи в XML: {e}")

def load_from_xml(filename: str) -> Dict[str, Any]:
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        data = {"users": [], "content": []}

        # Пользователи
        for user in root.find("users"):
            user_dict = {
                "user_id": int(user.get("user_id")),
                "username": user.get("username"),
                "email": user.get("email"),
                "is_active": user.get("is_active") == "true",
                "role": user.get("role")
            }
            if user_dict["role"] == "customer":
                phone_elem = user.find("phone")
                user_dict["phone"] = phone_elem.text if phone_elem is not None else ""
                sub_elem = user.find("subscription")
                if sub_elem is not None:
                    user_dict["subscription"] = {
                        "sub_id": int(sub_elem.get("sub_id")),
                        "plan_name": sub_elem.get("plan_name"),
                        "start_date": sub_elem.get("start_date"),
                        "end_date": sub_elem.get("end_date")
                    }
            data["users"].append(user_dict)

        content_elem = root.find("content")
        if content_elem is not None:
            for item in content_elem:
                item_dict = {
                    "content_id": int(item.get("content_id")),
                    "title": item.get("title"),
                    "release_year": int(item.get("release_year")),
                    "duration": int(item.get("duration")),
                    "description": item.find("description").text or ""
                }
                if item.tag == "movie":
                    item_dict["type"] = "movie"
                    item_dict["is_premiere"] = item.get("is_premiere") == "true"
                else:
                    item_dict["type"] = "series"
                    item_dict["seasons"] = int(item.get("seasons"))
                data["content"].append(item_dict)
        return data

    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return {"users": [], "content": []}
    except ET.ParseError as e:
        print(f"Ошибка чтения XML: {e}")
        return {"users": [], "content": []}