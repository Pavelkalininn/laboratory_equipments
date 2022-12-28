
import os

import pytest
from dotenv import (
    load_dotenv,
)
from telethon import (
    TelegramClient,
)
from telethon.sessions import (
    StringSession,
)

load_dotenv()

TELEGRAM_API_ID = int(os.environ["TELEGRAM_API_ID"])
TELEGRAM_API_HASH = os.environ["TELEGRAM_API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]


@pytest.fixture(scope="session")
async def client() -> TelegramClient:
    await client.connect()
    await client.get_me()
    await client.get_dialogs()

    yield TelegramClient(
        StringSession(SESSION_STRING), TELEGRAM_API_ID, TELEGRAM_API_HASH,
        sequential_updates=True
    )

    await client.disconnect()
    await client.disconnected
