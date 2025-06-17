from telethon import TelegramClient, events
from config.settings import API_ID, API_HASH, BOT_TOKEN, CHANNEL_ORIGEM
from domain.link_parser import extract_links, build_affiliate_link
from services.database import init_db, link_exists, save_link
from services.ai_classifier import is_relevant
from services.telegram_sender import send_to_channel
from services.notifier import notify_admin
from core.logger import setup_logger

logger = setup_logger()

client = TelegramClient("listener", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def start_listener():
    init_db()

    @client.on(events.NewMessage(chats=CHANNEL_ORIGEM))
    async def handler(event):
        text = event.message.message
        links = extract_links(text)

        for url in links:
            link_info = build_affiliate_link(url)
            if not link_info:
                continue
            if link_exists(link_info.afiliado_url):
                logger.info("Link já postado: %s", link_info.afiliado_url)
                continue
            if is_relevant(text):
                await send_to_channel(f"{text}\n\n🔗 {link_info.afiliado_url}")
                save_link(link_info.afiliado_url)
                logger.info("Promoção enviada para canal destino.")
            else:
                await notify_admin(f"Promoção rejeitada:\n{text}")
                logger.info("Promoção considerada irrelevante e notificada ao admin.")

    logger.info("Listener iniciado. Aguardando mensagens...")
    await client.run_until_disconnected()