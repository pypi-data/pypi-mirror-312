from typing import *
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter

try:
    from src.models import UserRole, User # type: ignore
except ImportError:
    class UserRole(Any): ...
    class User(Any): ...

class Role(Filter):
    def __init__(self, role: UserRole):
        self.role = role

    async def __call__(self, message: Message | CallbackQuery) -> bool:
        user: User | None = User.select().where(User.user_id == message.from_user.id).first()
        if user and user.role >= self.role:
            return True
        return False

class ChatType(Filter):
    def __init__(self, *type: str, exclude: List[str] = []):
        self.types = type
        self.exclude = exclude

    async def __call__(self, message: Message | CallbackQuery) -> bool:
        return message.chat.type in self.types and message.chat.type not in self.exclude if isinstance(message, Message)\
          else message.message.chat.type in self.types and message.message.chat.type not in self.exclude