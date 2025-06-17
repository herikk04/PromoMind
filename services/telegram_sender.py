# afiliado_bot/services/telegram_sender.py

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import logging
import asyncio

# Importa o BOT_TOKEN e DESTINATION_CHANNEL_ID das configurações
from config.settings import BOT_TOKEN, DESTINATION_CHANNEL_ID, RETRY_ATTEMPTS, RETRY_DELAY_SECONDS

logger = logging.getLogger(__name__)

class TelegramSender:
    """
    Classe responsável por enviar mensagens para o canal Telegram de destino.
    """
    def __init__(self, bot_token: str, destination_channel_id: int):
        """
        Inicializa o TelegramSender com o token do bot e o ID do canal de destino.

        Args:
            bot_token (str): O token do bot Telegram para enviar mensagens.
            destination_channel_id (int): O ID do canal onde as promoções serão postadas.
        """
        self.bot_token = bot_token
        self.destination_channel_id = destination_channel_id
        # Cria uma instância do cliente Telegram para o bot
        # 'bot' é o nome da sessão, pode ser qualquer string
        self.client = TelegramClient('bot_sender', None, None).start(bot_token=bot_token)
        logger.info(f"TelegramSender inicializado para o canal de destino: {self.destination_channel_id}")

    async def connect(self):
        """
        Conecta o cliente Telegram do sender. Tenta reconectar em caso de falha.
        """
        for attempt in range(RETRY_ATTEMPTS):
            try:
                logger.info(f"Tentando conectar o bot sender ao Telegram (tentativa {attempt + 1}/{RETRY_ATTEMPTS})...")
                # Certifica-se de que o bot está iniciado e conectado
                if not self.client.is_connected():
                     await self.client.start(bot_token=self.bot_token)
                logger.info("Bot sender conectado ao Telegram.")

                # Tenta entrar no canal de destino se ainda não estiver nele
                try:
                    await self.client(JoinChannelRequest(self.destination_channel_id))
                    logger.info(f"Garantido que o bot está no canal de destino: {self.destination_channel_id}")
                except Exception as e:
                    logger.warning(f"Bot não conseguiu entrar no canal {self.destination_channel_id} (pode já estar nele ou não ter permissão). Erro: {e}")

                return # Conexão bem-sucedida
            except Exception as e:
                logger.error(f"Erro ao conectar o bot sender ao Telegram: {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY_SECONDS) # Espera antes de tentar novamente
                else:
                    logger.critical("Falha crítica ao conectar o bot sender ao Telegram após múltiplas tentativas. Encerrando.")
                    raise # Re-levanta a exceção se todas as tentativas falharem

    async def send_promotion(self, message_text: str, affiliate_link: str):
        """
        Envia uma promoção para o canal de destino, substituindo o link original
        pelo link de afiliado.

        Args:
            message_text (str): O texto original da mensagem da promoção.
            affiliate_link (str): O link de afiliado a ser inserido.
        """
        # Substitui qualquer URL na mensagem original pelo link de afiliado
        # Esta é uma abordagem simples; para uma substituição mais precisa
        # você pode querer usar regex para encontrar o link original específico
        # e substituí-lo. Por simplicidade, assumimos que o link de afiliado
        # pode ser anexado ou substituir o primeiro link encontrado.
        
        # Uma forma mais robusta seria procurar o link original dentro da mensagem
        # e fazer a substituição exata. Por enquanto, vamos apenas adicionar
        # o link de afiliado ao final.
        
        # Cria a mensagem final para postagem
        # Você pode personalizar o formato da mensagem aqui.
        final_message = f"{message_text}\n\n🛒 Link da Oferta: {affiliate_link}"

        for attempt in range(RETRY_ATTEMPTS):
            try:
                await self.client.send_message(self.destination_channel_id, final_message)
                logger.info(f"Promoção enviada com sucesso para o canal de destino: {self.destination_channel_id}")
                return # Sai da função se a mensagem for enviada com sucesso
            except Exception as e:
                logger.error(f"Erro ao enviar promoção para o canal de destino (tentativa {attempt + 1}/{RETRY_ATTEMPTS}): {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY_SECONDS) # Espera antes de tentar novamente
                else:
                    logger.error("Falha ao enviar promoção após múltiplas tentativas.")

    async def disconnect(self):
        """
        Desconecta o cliente Telegram do sender.
        """
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            logger.info("Sender desconectado do Telegram.")

