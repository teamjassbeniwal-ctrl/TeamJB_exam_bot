import logging

from pymongo import ASCENDING

logger = logging.getLogger(__name__)


async def create_indexes(db) -> None:
    """Create Part 1 indexes. Idempotent: safe on every startup."""
    logger.info("Ensuring database indexes...")

    # Unique Telegram ID prevents duplicate registrations in Part 2.
    await db.users.create_index(
        [("telegram_id", ASCENDING)],
        unique=True,
        name="uniq_telegram_id",
    )

    logger.info("Indexes ready.")
