import httpx
import logging

http_client = httpx.AsyncClient(base_url="http://backend:8000", timeout=5.0)

async def get_client_in_backend(number: str):
    try:
        response = await http_client.get(f"/{number}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        return None

async def get_client_by_tg_id(id_tg: int):
    try:
        response = await http_client.get(f"/client_by_id/{id_tg}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logging.error(f"Ошибка API при поиске по ID: {e}")
        return None

async def get_client_by_id_thread(id_thread: int):
    try:
        response = await http_client.get(f"/client_by_id_thread/{id_thread}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logging.error(f"Ошибка API при поиске по ID: {e}")
        return None