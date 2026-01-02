import logging
from fastapi import APIRouter, HTTPException
from db.DBManager import DBManager
from db.connection import get_db_session
from schemas.CreateClientSchema import CreateClient

from schemas.CreateClientSchema import UpdateClient

logger = logging.getLogger(__name__)

update_client_router = APIRouter(tags=["Клиенты"])

@update_client_router.put("/update_client")
async def update_client(id_tg: int, data: UpdateClient):
    async with get_db_session() as db:
        manager = DBManager(db)
        result = await manager.manager_update_client(id_tg, data)
        if result is True:
            return {"message": "Изменения прошли успешно"}
        else:
            return {"message": "Пользователь не найден!"}