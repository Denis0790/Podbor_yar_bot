import aiosqlite
import logging
from schemas.CreateClientSchema import CreateClient, UpdateClient
from schemas.CreateOrderSchema import CreateOrder

logger = logging.getLogger(__name__)

class DBManager:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db


    async def manager_create_client(self, data: CreateClient):
        try:
            query = "INSERT INTO clients (id_tg, name, number, vin, id_thread) VALUES (?, ?, ?, ?, ?)"
            await self.db.execute(query, (data.id_tg, data.name, data.number, data.vin, data.id_thread))
            await self.db.commit()
            logger.info(f"Успешно добавлен клиент {data.name} (id_tg: {data.id_tg})")
        except Exception as e:
            logger.error(f"Ошибка при создании клиента в БД: {e}", exc_info=True)
            raise e

    async def manager_search_client(self, number: str):
        try:
            query = "SELECT * FROM clients WHERE number LIKE ?"
            search_pattern = f"%{number}%"
            cursor = await self.db.execute(query, (search_pattern,))
            client = await cursor.fetchone()
            if client is not None:
                client_data = dict(client)
                logger.info(f"Клиент {client_data} успешно найден!")
                return client_data
            else:
                logger.info(f"Клиент по номеру {number} не найден!")
                return None
        except Exception as e:
            logger.info(f"Ошибка при поиске клиента")
            raise e

    async def manager_update_client(self, id_tg: int, data: UpdateClient):
        try:
            update_data = data.model_dump(exclude_none=True)

            if not update_data:
                logger.warning("Нет данных для обновления")
                return False

            columns = [f"{key} = ?" for key in update_data.keys()]
            set_clause = ", ".join(columns)

            values = list(update_data.values())
            values.append(id_tg)

            query = f"UPDATE clients SET {set_clause} WHERE id_tg = ?"

            cursor = await self.db.execute(query, values)
            await self.db.commit()

            if cursor.rowcount == 0:
                logger.warning(f"Клиент с id_tg {id_tg} не найден.")
                return False

            logger.info(f"Клиент {id_tg} успешно обновлен. Изменены поля: {list(update_data.keys())}")
            return True

        except Exception as e:
            logger.error(f"Ошибка при обновлении клиента в БД: {e}", exc_info=True)
            return False

    async def manager_create_order(self, order: CreateOrder):
        try:
            query = "INSERT INTO orders (client_phone, description) VALUES (?, ?)"
            await self.db.execute(query, (order.client_phone, order.description))
            await self.db.commit()
            logger.info(f"Данные успешно добавлены")
        except Exception as e:
            logger.error(f"Ошибка при записи в БД: {e}", exc_info=True)
            return e

    async def manager_search_order(self, client_phone: str):
        try:
            query = "SELECT * FROM orders WHERE client_phone LIKE ?"
            search_pattern = f"%{client_phone}%"
            cursor = await self.db.execute(query, (search_pattern,))
            order = await cursor.fetchall()
            return order
        except Exception as e:
            raise e

    async def manager_search_client_by_tg_id(self, id_tg: int):
        try:
            query = "SELECT * FROM clients WHERE id_tg = ?"

            cursor = await self.db.execute(query, (id_tg,))
            client = await cursor.fetchone()

            if client is not None:
                client_data = dict(client)
                logger.info(f"Клиент {id_tg} успешно найден!")
                return client_data
            else:
                logger.info(f"Клиент с id_tg {id_tg} не найден!")
                return None

        except Exception as e:
            logger.error(f"Ошибка при поиске клиента по id_tg {id_tg}: {e}")
            raise e

    async def manager_search_client_by_id_thread(self, id_thread: int):
        try:
            query = "SELECT * FROM clients WHERE id_thread = ?"

            cursor = await self.db.execute(query, (id_thread,))
            client = await cursor.fetchone()

            if client is not None:
                client_data = dict(client)
                logger.info(f"Клиент {id_thread} успешно найден!")
                return client_data
            else:
                logger.info(f"Клиент с id_tg {id_thread} не найден!")
                return None

        except Exception as e:
            logger.error(f"Ошибка при поиске клиента по id_tg {id_thread}: {e}")
            raise e

