import httpx
import logging

http_client = httpx.AsyncClient(base_url="http://backend:8000", timeout=5.0)

async def get_info_in_backend(number: str):
    try:
        response = await http_client.get(f"/description{number}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        return None