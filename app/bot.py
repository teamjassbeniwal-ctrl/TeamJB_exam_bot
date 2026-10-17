import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from app.config import load_config
from app.database.connection import close_mongo, get_database, init_mongo
from app.database.indexes import create_indexes

logger = logging.getLogger("teamjb")


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


async def cmd_start(message: Message) -> None:
    user = message.from_user
    await message.answer(
        "Team JB AI Exam Preparation\n\n"
        f"Hello {user.full_name}.\n"
        f"Your Telegram ID: {user.id}\n\n"
        "Part 1 running: bot is alive and MongoDB is connected.\n"
        "Registration and exam selection arrive in Part 2."
    )


async def main() -> None:
    config = load_config()
    setup_logging(config.log_level)

    logger.info("Starting Team JB AI Exam Preparation Bot (Part 1)...")

    await init_mongo(config.mongodb_uri, config.mongodb_db)
    db = get_database()
    await create_indexes(db)

    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(cmd_start, CommandStart())

    try:
        logger.info("Bot is polling. Send /start in Telegram to test.")
        await dp.start_polling(bot)
    finally:
        logger.info("Shutting down...")
        await bot.session.close()
        await close_mongo()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Interrupted by user.")
    except Exception:
        logger.exception("Fatal error during startup.")
        sys.exit(1)
