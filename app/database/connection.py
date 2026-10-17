import logging
from typing import Optional

from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

logger = logging.getLogger(__name__)

_client: Optional[AsyncMongoClient] = None
_db_name: Optional[str] = None


async def init_mongo(uri: str, db_name: str) -> AsyncMongoClient:
    """Connect to MongoDB Atlas and verify with a ping. Idempotent."""
    global _client, _db_name

    if _client is not None:
        logger.warning("init_mongo called again; reusing existing client")
        return _client

    logger.info("Connecting to MongoDB Atlas (database=%s)...", db_name)
    client = AsyncMongoClient(
        uri,
        server_api=ServerApi(version="1", strict=True, deprecation_errors=True),
    )

    try:
        await client.admin.command("ping")
    except Exception:
        await client.close()
        logger.exception(
            "MongoDB ping failed. Check MONGODB_URI and Atlas Network Access."
        )
        raise

    _client = client
    _db_name = db_name
    logger.info("MongoDB connected successfully.")
    return client


def get_database():
    if _client is None or _db_name is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongo() first.")
    return _client[_db_name]


def get_client() -> AsyncMongoClient:
    if _client is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongo() first.")
    return _client


async def close_mongo() -> None:
    global _client, _db_name
    if _client is not None:
        await _client.close()
        logger.info("MongoDB connection closed.")
    _client = None
    _db_name = None
