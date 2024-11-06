import logging
from datetime import date
from typing import Optional
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

# from tldl.schema import Feed


router = Router(name="commands-router")
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        """
        Привет, я умею сокращать лекции, просто отправь мне файл лекции (именно файл), а я напишу тебе когда закончу
        /ᐠ｡ꞈ｡ᐟ\
        """
    )


# @router.message(Command("status"))
# async def cmd_status(message: Message, session: AsyncSession):
#     current_date = date.today()
#     current_feeder: Optional[Feed] = await session.get(Feed, current_date)
#     if current_feeder is not None:
#         await message.answer(f"Сегодня Бусю кормит @{current_feeder.feeder}!")
#     else:
#         await message.answer("Пока никто не кормит Бусю :c")


# @router.message(Command("feed"))
# async def cmd_feed(message: Message, session: AsyncSession):
#     current_date = date.today()
#     current_feeder: Optional[Feed] = await session.get(Feed, current_date)
#     if message.from_user is None:
#         logging.warn("Unable to check the sender of a message")
#         return

#     if current_feeder is not None:
#         current_feeder.feeder = message.from_user.username
#     else:
#         current_feeder = Feed(day=current_date, feeder=message.from_user.username)

#     await session.merge(current_feeder)
#     await session.flush()

#     feed_msg = await message.answer(
#         f"{current_date} Бусю будет кормить @{current_feeder.feeder}, спасибо <3"
#     )

#     await message.bot.pin_chat_message(message.chat.id, feed_msg.message_id)