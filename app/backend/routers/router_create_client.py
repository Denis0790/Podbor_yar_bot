import logging
from fastapi import APIRouter, HTTPException
from db.DBManager import DBManager
from db.connection import get_db_session
from schemas.CreateClientSchema import CreateClient

logger = logging.getLogger(__name__)

create_client_router = APIRouter(tags=["Клиенты"])


@create_client_router.post("/add")
async def create_client(client: CreateClient):
    async with get_db_session() as db:
        manager = DBManager(db)
        check_client = await manager.manager_search_client(client.number)

        if check_client is not None:
            raise HTTPException(
                status_code=400,
                detail="Клиент с таким номером уже существует!"
            )
        try:
            await manager.manager_create_client(client)
            return {"status": "success", "message": "Регистрация прошла успешно!"}
        except Exception as e:
            if "UNIQUE constraint failed: clients.id_tg" in str(e):
                raise HTTPException(status_code=400, detail="Ваш Telegram ID уже есть в базе!")

            logger.error(f"Системная ошибка: {e}")
            raise HTTPException(status_code=500, detail="Ошибка на стороне сервера")