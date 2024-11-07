import io
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from tempfile import NamedTemporaryFile

from tldl.adapters import VideoRepository, create_boto_client
from tldl.settings import settings

from tldl.schema import VideoProcessing, VideoStatus

router = Router(name="commands-router")
logger = logging.getLogger(__name__)

video_repo = VideoRepository(
    settings.bucket_name,
    create_boto_client(
        settings.s3_endpoint, settings.s3_access_key_id, settings.s3_secret_access_key
    ),
)


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

    tg_file = await message.bot.get_file(message.document.file_id)
    with NamedTemporaryFile(mode="+w", suffix=".mp4") as tmp_file:
        await message.bot.download_file(tg_file.file_path, tmp_file.name)
        video_repo.upload_file(tg_file.file_unique_id + ".mp4", tmp_file.name)

    processing = VideoProcessing(
        status=VideoStatus.created,
        chat_id=str(message.chat.id),
        msg_id=str(message.message_id),
        raw_file_path=message.document.file_name,
    )

    await session.merge(processing)
    await session.flush()

    await message.answer("Твой файл принят на обработку, ожидай ответное сообщение")
