import io
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from tempfile import NamedTemporaryFile

from tldl.adapters import VideoRepository, init_minio_client
from tldl.settings import settings


router = Router(name="commands-router")
logger = logging.getLogger(__name__)
video_repo = VideoRepository(settings.bucket_name, init_minio_client)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        """
        Привет, я умею сокращать лекции, просто отправь мне файл лекции (именно файл), а я напишу тебе когда закончу
        /ᐠ｡ꞈ｡ᐟ\
        """
    )


@router.message()
async def handle_file(message: Message, session: AsyncSession):
    if message.document is None:
        await message.reply(
            "В твоем сообщении нет файла, убедись, что ты отправляешь лекцию как файл, а не видео!"
        )
        return

    if message.document.file_id is None:
        logging.error("Unable to get document file id")
        return

    if not message.document.file_name.endswith(".mp4"):
        await message.reply("Пока TLDL поддерживает только mp4")
        return

    with NamedTemporaryFile("+w", suffix=".mp4") as user_file:
        file_bytes_io: io.BytesIO = message.bot.download_file(user_file.name)
        res = video_repo.upload_file(message.document.file_name, file_bytes_io)
        # save uploaded to db
        file_bytes_io.close()
        
    await session.flush()

    await message.answer("Твой файл принят на обработку, ожидай ответное сообщение")
