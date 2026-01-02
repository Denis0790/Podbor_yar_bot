from dataclasses import dataclass

@dataclass
class DataRegistrationClient:
    id_tg: int
    name: str
    number: str
    vin: str
    id_thread: int

@dataclass
class DataUpdateClient:
    name: str
    number: str
    vin: str