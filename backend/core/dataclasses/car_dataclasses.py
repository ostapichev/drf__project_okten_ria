from dataclasses import dataclass
from datetime import datetime

from core.dataclasses.user_dataclasses import UserDataClass


@dataclass
class CarDataClass:
    id: int
    brand: str
    model: str
    price: int
    year: int
    content: str
    created_at: datetime
    updated_at: datetime
    user: UserDataClass
