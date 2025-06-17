# afiliado_bot/services/notifier.py

from telethon import TelegramClient
import logging
import asyncio

# Importa o BOT_TOKEN e ADMIN_CHAT_ID das configurações
from config.settings import BOT_TOKEN, ADMIN_CHAT_ID, RETRY_ATTEMPTS, RETRY_DELAY_SECONDS

logger = logging.getLogger(__name__)

class Notifier:
    """
    Classe responsável por enviar notificações privadas para o administrador.
    """
    def __init__(self, bot_token: str, admin_chat_id: int):
        """
        Inicializa o Notifier com o token do bot e o ID do chat do administrador.

        Args:
            bot_token (str): O token do bot Telegram para enviar mensagens.
            admin_chat_id (int): O ID do chat pessoal do administrador.
        """
        self.bot_token = bot_token
        self.admin_chat_id = admin_chat_id
        # Cria uma instância do cliente Telegram para o bot
        # 'bot' é o nome da sessão, pode ser qualquer string
        self.client = TelegramClient('bot_notifier', None, None).start(bot_token=bot_token)
        logger.info(f"Notifier inicializado para o chat do administrador: {self.admin_chat_id}")

    async def send_admin_notification(self, message: str):
        """
        Envia uma mensagem de notificação para o chat do administrador.

        Args:
            message (str): O texto da mensagem de notificação.
        """
        for attempt in range(RETRY_ATTEMPTS):
            try:
                await self.client.send_message(self.admin_chat_id, message)
                logger.info(f"Notificação enviada ao administrador: {message[:100]}...")
                return # Sai da função se a mensagem for enviada com sucesso
            except Exception as e:
                logger.error(f"Erro ao enviar notificação ao administrador (tentativa {attempt + 1}/{RETRY_ATTEMPTS}): {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY_SECONDS) # Espera antes de tentar novamente
                else:
                    logger.error("Falha ao enviar notificação ao administrador após múltiplas tentativas.")

    async def disconnect(self):
        """
        Desconecta o cliente Telegram do notifier.
        """
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            logger.info("Notifier desconectado do Telegram.")

