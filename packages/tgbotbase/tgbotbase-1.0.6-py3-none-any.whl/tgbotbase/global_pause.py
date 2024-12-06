from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from typing import * 
import os 

from tgbotbase.filters import Role, PauseFilter

try:
    from src.models import UserRole, User # type: ignore
except ImportError:
    class UserRole(Any): ...
    class User(Any): ...

from tgbotbase.utils import SHARED_OBJECTS

dp = SHARED_OBJECTS["dp"]

os.environ["GLOBAL_PAUSE"] = "false"

@dp.message(Role(UserRole.ADMIN.value), Command("pause"))
async def pause(message: Message):
    os.environ["GLOBAL_PAUSE"] = "true"
    await message.answer("Paused")

@dp.message(Role(UserRole.ADMIN.value), PauseFilter(), Command("unpause"))
async def unpause(message: Message):
    os.environ["GLOBAL_PAUSE"] = "false"
    await message.answer("Unpaused")

@dp.callback_query(PauseFilter())
@dp.message(PauseFilter())
async def paused(message: Message | CallbackQuery, user: User):
    pass