import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from tldl.settings import settings
from tldl.handlers import commands
from tldl.middlewares import DbSessionMiddleware


async def run_bot():
    engine = create_async_engine(url=settings.pg_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    
    localserver = AiohttpSession(api=TelegramAPIServer.from_base(settings.tg_api_server))
    bot = Bot(token=settings.bot_token, session=localserver)

    # Setup dispatcher and bind routers to it
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    # Register handlers
    dp.include_router(commands.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()