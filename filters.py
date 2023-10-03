from aiogram.filters import Filter
from aiogram.types import Message
from settings import ADMIN_USER_IDS


class is_admin(Filter):
    key = 'is_admin'

    async def check(self, message: Message) -> bool:
        return str(message.from_user.id) in ADMIN_USER_IDS