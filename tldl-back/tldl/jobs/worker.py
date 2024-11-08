import asyncio
import dataclasses
import logging
from tempfile import NamedTemporaryFile

from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from tldl.settings import settings
from tldl.adapters import VideoRepository, create_boto_client
from tldl.schema import VideoProcessing, VideoStatus
from tldl.logic import (
    Chapter,
    CopyFileHandler,
    SilenceCutHandler,
    TranscriberHandler,
    ChaptersHandler,
    TldlContext,
    SummarizerHandler,
)

video_repo = VideoRepository(
    settings.bucket_name,
    create_boto_client(
        settings.s3_endpoint, settings.s3_access_key_id, settings.s3_secret_access_key
    ),
)


async def send_notifications():
    logger = logging.getLogger(__name__ + ":notification-processor")

    localserver = AiohttpSession(
        api=TelegramAPIServer.from_base(settings.tg_api_server)
    )
    bot = Bot(token=settings.bot_token, session=localserver)

    engine = create_async_engine(url=settings.pg_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    while True:
        await asyncio.sleep(1)
        async with sessionmaker() as session:
            async with session.begin():
                query = (
                    select(VideoProcessing)
                    .where(VideoProcessing.status == VideoStatus.cleaned)
                    .with_for_update(skip_locked=True)
                    .limit(1)
                )

                query_result = await session.execute(query)
                processed_video = query_result.scalar()
                if processed_video == None:
                    logger.info("No records to notify yet")
                else:
                    with NamedTemporaryFile("+w", suffix=".mp4") as tmp_file:
                        video_repo.get_file(
                            processed_video.ready_file_path, tmp_file.name
                        )
                        tg_fs_input_file = FSInputFile(
                            tmp_file.name, filename=processed_video.ready_file_path
                        )
                        video_msg = await bot.send_document(
                            document=tg_fs_input_file,
                            chat_id=processed_video.chat_id,
                            reply_to_message_id=processed_video.msg_id,
                        )

                        chapters = list(
                            map(
                                lambda x: Chapter(**x),
                                processed_video.meta.get("chapters", []),
                            )
                        )
                        msg_header = ", ".join(processed_video.meta.get("hashtags", []))
                        msg_text = (
                            msg_header
                            + "\n"
                            + "\n".join(list(map(lambda x: str(x), chapters)))
                        )

                        await bot.send_message(
                            text=msg_text,
                            chat_id=video_msg.chat.id,
                            reply_to_message_id=video_msg.message_id,
                            parse_mode=ParseMode.MARKDOWN,
                        )
                    query = (
                        update(VideoProcessing)
                        .where(VideoProcessing.uid == processed_video.uid)
                        .values(status=VideoStatus.notified)
                    )
                    await session.execute(query)
                await session.commit()


async def process_records():
    logger = logging.getLogger(__name__ + ":video-processor")

    localserver = AiohttpSession(
        api=TelegramAPIServer.from_base(settings.tg_api_server)
    )
    bot = Bot(token=settings.bot_token, session=localserver)

    engine = create_async_engine(url=settings.pg_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    tldl_handler = CopyFileHandler().set_next(
        SilenceCutHandler().set_next(
            TranscriberHandler().set_next(
                SummarizerHandler().set_next(ChaptersHandler())
            )
        )
    )

    while True:
        try:
            await asyncio.sleep(1)
            async with sessionmaker() as session:
                async with session.begin():
                    query = (
                        select(VideoProcessing)
                        .where(VideoProcessing.status == VideoStatus.created)
                        .with_for_update(skip_locked=True)
                        .limit(1)
                    )

                    query_result = await session.execute(query)
                    new_created_video = query_result.scalar()
                    if new_created_video == None:
                        logger.info("No records to process yet")
                    else:
                        with NamedTemporaryFile("+w", suffix=".mp4") as tmp_file:
                            video_repo.get_file(
                                new_created_video.raw_file_path, tmp_file.name
                            )

                            handler_ctx = TldlContext(source_filename=tmp_file.name)
                            tldl_handler.handle(handler_ctx)

                            video_repo.upload_file(
                                handler_ctx.source_filename, handler_ctx.source_filename
                            )

                            logger.info("Finished processing for video")
                            new_created_video.meta["chapters"] = list(
                                map(
                                    lambda x: dataclasses.asdict(x),
                                    handler_ctx.chapters,
                                )
                            )
                            new_created_video.meta["hashtags"] = (
                                handler_ctx.code_list or []
                            )

                            query = (
                                update(VideoProcessing)
                                .where(VideoProcessing.uid == new_created_video.uid)
                                .values(
                                    status=VideoStatus.cleaned,
                                    ready_file_path=handler_ctx.source_filename,
                                    meta=new_created_video.meta,
                                )
                            )
                            await session.execute(query)

                    await session.commit()

        except Exception as e:
            logger.error("Error while processing records %s", e)


async def run_worker():
    await asyncio.gather(send_notifications(), process_records())


def _main():
    asyncio.run(run_worker())


if __name__ == "__main__":
    _main()
