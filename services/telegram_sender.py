from telethon.sync import TelegramClient
from config.settings import API_ID, API_HASH, BOT_TOKEN, CHANNEL_DESTINO

client = TelegramClient("sender", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def send_to_channel(message):
    async with client:
        await client.send_message(CHANNEL_DESTINO, message)