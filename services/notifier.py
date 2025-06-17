from telethon.sync import TelegramClient
from config.settings import API_ID, API_HASH, ADMIN_CHAT_ID

client = TelegramClient("notifier", API_ID, API_HASH)

async def notify_admin(message):
    async with client:
        await client.send_message(ADMIN_CHAT_ID, message)
