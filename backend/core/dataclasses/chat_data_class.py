from dataclasses import dataclass

from core.dataclasses.user_dataclasses import UserDataClass


@dataclass
class ChatDataClass:
    id: int
    message: str
    owner: UserDataClass
