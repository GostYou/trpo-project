import logging

import uvicorn
from fastapi import FastAPI

from src.controllers.products import router as memberships_router

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gym Membership API",
    description="API для управления абонементами тренажерного зала",
    version="1.0.0",
)

app.include_router(memberships_router)

@app.get("/")
async def root():
    return {
        "message": "Это API для управления абонементами тренажерного зала",
        "endpoints": {
            "GET /memberships": "Получить все абонементы (с сортировкой по type)",
            "GET /memberships/{id}": "Получить абонемент по ID",
            "POST /memberships": "Создать новый абонемент",
            "PUT /memberships/{id}": "Обновить существующий абонемент",
            "DELETE /memberships/{id}": "Удалить абонемент"
        }
    }

def main():
    logger.info('Started')
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

if __name__ == "__main__":
    main()