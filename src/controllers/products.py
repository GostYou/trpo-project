from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import json
import os

router = APIRouter(prefix="/memberships", tags=["memberships"])

DATA_FILE = "memberships.json"

# Модель абонемента
class Membership:
    def __init__(self, id: int, type: str, price: float, validity_days: int, classes_count: int):
        self.id = id
        self.type = type
        self.price = price
        self.validity_days = validity_days
        self.classes_count = classes_count
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "price": self.price,
            "validity_days": self.validity_days,
            "classes_count": self.classes_count
        }

# Функции для работы с JSON файлом
def load_memberships():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        # Начальные данные
        initial_data = [
            {"id": 1, "type": "Дневной", "price": 3000, "validity_days": 30, "classes_count": 10},
            {"id": 2, "type": "Вечерний", "price": 4000, "validity_days": 30, "classes_count": 10},
            {"id": 3, "type": "Безлимитный", "price": 6000, "validity_days": 30, "classes_count": 999},
            {"id": 4, "type": "Годовой", "price": 45000, "validity_days": 365, "classes_count": 999},
            {"id": 5, "type": "Пробный", "price": 500, "validity_days": 7, "classes_count": 1},
            {"id": 6, "type": "Студенческий", "price": 2500, "validity_days": 30, "classes_count": 8}
        ]
        save_memberships(initial_data)
        return initial_data

def save_memberships(memberships):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(memberships, file, ensure_ascii=False, indent=2)

# GET: Получить список всех абонементов с сортировкой
@router.get("/")
async def get_memberships(sorting: Optional[str] = Query(None, pattern="^(asc|desc)$")):
    """
    Получить список всех абонементов
    
    - **sorting**: параметр сортировки по названию (asc - по возрастанию, desc - по убыванию)
    """
    memberships = load_memberships()
    
    if sorting:
        reverse = sorting == "desc"
        memberships.sort(key=lambda x: x["type"], reverse=reverse)
    
    return {
        "memberships": memberships,
        "total": len(memberships)
    }

# GET: Получить абонемент по ID
@router.get("/{membership_id}")
async def get_membership(membership_id: int):
    """
    Получить абонемент по его ID
    """
    memberships = load_memberships()
    membership = next((m for m in memberships if m["id"] == membership_id), None)
    
    if membership is None:
        raise HTTPException(status_code=404, detail="Абонемент не найден")
    
    return membership

# POST: Создать новый абонемент
@router.post("/")
async def create_membership(
    type: str, 
    price: float, 
    validity_days: int, 
    classes_count: int
):
    """
    Создать новый абонемент
    
    - **type**: тип абонемента (например: "Дневной", "Вечерний")
    - **price**: цена в рублях
    - **validity_days**: срок действия в днях
    - **classes_count**: количество занятий
    """
    memberships = load_memberships()
    
    # Генерация нового ID
    new_id = max([m["id"] for m in memberships], default=0) + 1
    
    new_membership = {
        "id": new_id,
        "type": type,
        "price": price,
        "validity_days": validity_days,
        "classes_count": classes_count
    }
    
    memberships.append(new_membership)
    save_memberships(memberships)
    
    return new_membership

# PUT: Обновить существующий абонемент
@router.put("/{membership_id}")
async def update_membership(
    membership_id: int, 
    type: Optional[str] = None, 
    price: Optional[float] = None, 
    validity_days: Optional[int] = None, 
    classes_count: Optional[int] = None
):
    """
    Обновить существующий абонемент
    
    - **membership_id**: ID абонемента для обновления
    - **type**: новый тип абонемента (опционально)
    - **price**: новая цена (опционально)
    - **validity_days**: новый срок действия (опционально)
    - **classes_count**: новое количество занятий (опционально)
    """
    memberships = load_memberships()
    membership_index = next((i for i, m in enumerate(memberships) if m["id"] == membership_id), None)
    
    if membership_index is None:
        raise HTTPException(status_code=404, detail="Абонемент не найден")
    
    # Обновление только переданных полей
    if type is not None:
        memberships[membership_index]["type"] = type
    if price is not None:
        memberships[membership_index]["price"] = price
    if validity_days is not None:
        memberships[membership_index]["validity_days"] = validity_days
    if classes_count is not None:
        memberships[membership_index]["classes_count"] = classes_count
    
    save_memberships(memberships)
    
    return memberships[membership_index]

# DELETE: Удалить абонемент
@router.delete("/{membership_id}")
async def delete_membership(membership_id: int):
    """
    Удалить абонемент по его ID
    """
    memberships = load_memberships()
    membership_index = next((i for i, m in enumerate(memberships) if m["id"] == membership_id), None)
    
    if membership_index is None:
        raise HTTPException(status_code=404, detail="Абонемент не найден")
    
    deleted_membership = memberships.pop(membership_index)
    save_memberships(memberships)
    
    return {"message": "Абонемент удален", "deleted_membership": deleted_membership}