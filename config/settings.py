import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ORIGEM = os.getenv("CHANNEL_ORIGEM")
CHANNEL_DESTINO = os.getenv("CHANNEL_DESTINO")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AFILIADOS = {
    "amazon.com.br": "?tag=SEU_CODIGO",
    "aliexpress.com": "?aff_fcid=SEU_CODIGO",
    "mercadolivre.com.br": "?mkt_referrer=SEU_CODIGO",
    "magazineluiza.com.br": "?partner_id=SEU_CODIGO",
    "shopee.com.br": "?utm_source=SEU_CODIGO",
}
