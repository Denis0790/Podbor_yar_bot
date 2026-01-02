from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ClientBase(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=20)
    number: Optional[str] = Field(None, description="Телефон")
    vin: Optional[str] = Field(None, min_length=17, max_length=17)

    @field_validator('name')
    @classmethod
    def detailed_name_check(cls, n: Optional[str]) -> Optional[str]:
        if n is None: return n
        if not (2 <= len(n) <= 20):
            raise ValueError("Имя должно быть от 2 до 20 символов")
        return n

    @field_validator('number')
    @classmethod
    def detailed_number_check(cls, nu: Optional[str]) -> Optional[str]:
        if nu is None: return nu
        if not (10 <= len(nu) <= 12):
            raise ValueError("Некорректная длина номера телефона")
        return nu

    @field_validator('vin')
    @classmethod
    def detailed_vin_check(cls, v: Optional[str]) -> Optional[str]:
        if v is None: return v
        v = v.strip().upper()
        if len(v) != 17:
            raise ValueError("VIN должен содержать ровно 17 символов")
        return v

class CreateClient(ClientBase):
    id_tg: int
    name: str
    number: str
    vin: str
    id_thread: Optional[int] = None

class UpdateClient(ClientBase):
    pass