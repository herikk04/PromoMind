# afiliado_bot/config/settings.py

import os

# --- Configurações do Telegram ---
API_ID = int(os.getenv("TELEGRAM_API_ID", "SEU_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "SEU_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_BOT_TOKEN")

# IDs dos canais e chats
# Obtenha o ID do canal de origem (ex: @canal_promocoes)
# Você pode encaminhar uma mensagem do canal para o @RawDataBot no Telegram
# O ID será algo como -1001234567890
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID", -1234567890)) # Substitua pelo ID do seu canal de origem
DESTINATION_CHANNEL_ID = int(os.getenv("DESTINATION_CHANNEL_ID", -1234567891)) # Substitua pelo ID do seu canal de destino
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 123456789)) # Substitua pelo seu ID de chat pessoal para notificações

# --- Configurações da OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_OPENAI")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o") # Ou outro modelo como "gpt-3.5-turbo"

# Prompt para a IA classificar a relevância da promoção
IA_PROMPT_TEMPLATE = """
Você é um especialista em promoções de e-commerce. Sua tarefa é analisar o texto de uma promoção e determinar se ela é relevante para um canal de ofertas.
Considere como relevante promoções com descontos significativos, cupons, ofertas de "leve 2 pague 1", ou preços muito abaixo do normal.
Ignore promoções genéricas, propagandas de serviços, ou produtos sem um desconto claro.

Responda APENAS com "sim" se a promoção for relevante e "não" se for irrelevante.

Texto da promoção:
"{promotion_text}"
"""

# --- Configurações de Afiliados ---
# Dicionário com os códigos de afiliado e regras de construção de link
# A chave é o domínio base, e o valor é um dicionário com 'affiliate_id' e 'param'
AFFILIATE_CONFIG = {
    "amazon.com.br": {
        "affiliate_id": os.getenv("AFFILIATE_ID_AMAZON", "seu_id_amazon-20"), # Exemplo: seu_id_amazon-20
        "param": "tag"
    },
    "aliexpress.com": {
        "affiliate_id": os.getenv("AFFILIATE_ID_ALIEXPRESS", "seu_id_aliexpress"), # Exemplo: 200000000_123456789
        "param": "aff_platform", # Aliexpress usa "albpm" ou similar, pode variar, ajuste conforme necessário
        "extra_params": {"albpt": "test", "sku_id": "123"} # Exemplo de parâmetros extras se necessário
    },
    "mercadolivre.com.br": {
        "affiliate_id": os.getenv("AFFILIATE_ID_MERCADOLIVRE", "seu_id_mercadolivre"), # Exemplo: ID do seu programa
        "param": "c_id" # Exemplo, o parâmetro real pode variar (e.g., "matt_test")
    },
    "magazineluiza.com.br": {
        "affiliate_id": os.getenv("AFFILIATE_ID_MAGALU", "seu_id_magalu"), # Exemplo: magalu-seuid
        "param": "utm_source", # Magalu geralmente usa utm_source ou similar para rastreamento
        "extra_params": {"utm_campaign": "bot_promocoes", "utm_medium": "telegram"}
    },
    "shopee.com.br": {
        "affiliate_id": os.getenv("AFFILIATE_ID_SHOPEE", "seu_id_shopee"), # Exemplo: shopee_seuid
        "param": "af_linkid" # O parâmetro real pode variar
    }
}

# --- Configurações do Banco de Dados ---
DATABASE_NAME = os.getenv("DATABASE_NAME", "posted_links.db")

# --- Configurações de Retry ---
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", 5))

