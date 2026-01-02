from pydantic import BaseModel


class CreateOrder(BaseModel):
    client_phone: str
    description: str