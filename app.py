# afiliado_bot/app.py

import asyncio
from telethon import events
import logging

# Importa as configurações do arquivo settings.py
from config.settings import (
    API_ID, API_HASH, BOT_TOKEN,
    SOURCE_CHANNEL_ID, DESTINATION_CHANNEL_ID, ADMIN_CHAT_ID,
    AFFILIATE_CONFIG
)

# Importa os módulos de serviço e domínio
from core.logger import setup_logging
from services.telegram_listener import TelegramListener
from services.telegram_sender import TelegramSender
from services.database import Database
from services.ai_classifier import AIClassifier
from services.notifier import Notifier
from domain.link_parser import LinkParser

# Configura o logger
setup_logging()
logger = logging.getLogger(__name__)

async def main():
    """
    Função principal que inicializa e executa o bot de monitoramento de promoções.
    """
    logger.info("Iniciando o bot de monitoramento de promoções...")

    # Inicializa o banco de dados SQLite
    db = Database()
    await db.init_db()

    # Inicializa os serviços
    listener = TelegramListener(API_ID, API_HASH)
    sender = TelegramSender(BOT_TOKEN, DESTINATION_CHANNEL_ID)
    notifier = Notifier(BOT_TOKEN, ADMIN_CHAT_ID)
    ai_classifier = AIClassifier()
    link_parser = LinkParser(AFFILIATE_CONFIG)

    # Conecta-se ao Telegram
    await listener.connect()
    await sender.connect()

    logger.info(f"Monitorando o canal de origem ID: {SOURCE_CHANNEL_ID}")

    @listener.client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID))
    async def handler(event):
        """
        Handler para novas mensagens no canal de origem.
        Processa a mensagem para extrair, classificar e repostar promoções.
        """
        message_text = event.message.message
        logger.info(f"Nova mensagem recebida: {message_text[:100]}...")

        # 1. Extrair e validar links
        valid_links = link_parser.extract_and_validate_links(message_text)

        if not valid_links:
            logger.info("Nenhum link válido encontrado na mensagem.")
            return

        for original_link in valid_links:
            # 2. Verificar duplicidade no banco de dados
            if await db.is_link_posted(original_link):
                logger.info(f"Link já postado, ignorando: {original_link}")
                continue

            # 3. Gerar link de afiliado
            affiliate_link = link_parser.generate_affiliate_link(original_link)
            if not affiliate_link:
                logger.warning(f"Não foi possível gerar link de afiliado para: {original_link}")
                await notifier.send_admin_notification(
                    f"Erro ao gerar link de afiliado para: {original_link}\n"
                    f"Mensagem original: {message_text[:500]}..."
                )
                continue

            # 4. Classificação por IA
            relevance = await ai_classifier.classify_relevance(message_text)

            if relevance == "sim":
                # 5. Publicar no canal de destino
                await sender.send_promotion(message_text, affiliate_link)
                await db.add_posted_link(original_link)
                logger.info(f"Promoção relevante postada: {affiliate_link}")
            else:
                # 6. Enviar notificação ao administrador se a IA rejeitar
                logger.info(f"Promoção irrelevante (IA): {message_text[:100]}...")
                await notifier.send_admin_notification(
                    f"Promoção rejeitada pela IA:\n"
                    f"Mensagem original: {message_text}\n"
                    f"Link original: {original_link}\n"
                    f"Link de afiliado gerado: {affiliate_link}\n"
                    f"Verifique manualmente."
                )

    # Mantém o cliente do listener rodando até ser desconectado
    await listener.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot desligado pelo usuário (Ctrl+C).")
    except Exception as e:
        logger.exception(f"Erro inesperado no app principal: {e}")

