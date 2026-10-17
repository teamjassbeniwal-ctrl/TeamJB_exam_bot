import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    mongodb_uri: str
    mongodb_db: str
    admin_ids: tuple[int, ...] = field(default_factory=tuple)
    log_level: str = "INFO"


def _parse_admin_ids(raw: str) -> tuple[int, ...]:
    if not raw.strip():
        return ()
    ids: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError as exc:
            raise ValueError(f"Invalid ADMIN_IDS entry: {part!r}") from exc
    return tuple(ids)


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb+srv://teamjb:jassbeniwal2005jb@cluster0.kqbahzq.mongodb.net/?retryWrites=true&w=majority").strip()
    mongodb_db = os.getenv("MONGODB_DB", "teamjb_exam_bot").strip()
    admin_ids_raw = os.getenv("ADMIN_IDS", "1955406483")
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    missing: list[str] = []
    if not bot_token:
        missing.append("BOT_TOKEN")
    if not mongodb_uri:
        missing.append("MONGODB_URI")

    if missing:
        raise ValueError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Check your .env file against .env.example."
        )

    return Config(
        bot_token=bot_token,
        mongodb_uri=mongodb_uri,
        mongodb_db=mongodb_db,
        admin_ids=_parse_admin_ids(admin_ids_raw),
        log_level=log_level,
    )
