# afiliado_bot/services/telegram_listener.py

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import logging
import asyncio

# Importa as configurações do Telegram
from config.settings import API_ID, API_HASH, RETRY_ATTEMPTS, RETRY_DELAY_SECONDS, SOURCE_CHANNEL_ID

logger = logging.getLogger(__name__)

class TelegramListener:
    """
    Classe responsável por escutar novas mensagens em um canal Telegram específico.
    """
    def __init__(self, api_id: int, api_hash: str):
        """
        Inicializa o TelegramListener com as credenciais da API.

        Args:
            api_id (int): O API ID da sua aplicação Telegram.
            api_hash (str): O API Hash da sua aplicação Telegram.
        """
        self.api_id = api_id
        self.api_hash = api_hash
        # Cria uma instância do cliente Telegram
        # 'session_name' é o nome do arquivo de sessão que será criado (ex: my_session.session)
        self.client = TelegramClient('listener_session', self.api_id, self.api_hash)
        logger.info("TelegramListener inicializado.")

    async def connect(self):
        """
        Conecta o cliente Telegram. Tenta reconectar em caso de falha.
        """
        for attempt in range(RETRY_ATTEMPTS):
            try:
                logger.info(f"Tentando conectar ao Telegram (tentativa {attempt + 1}/{RETRY_ATTEMPTS})...")
                # Inicia a sessão; se for a primeira vez, pedirá o número de telefone
                await self.client.start()
                logger.info("Conectado ao Telegram.")

                # Tenta entrar no canal de origem se ainda não estiver nele
                try:
                    await self.client(JoinChannelRequest(SOURCE_CHANNEL_ID))
                    logger.info(f"Garantido que o cliente está no canal de origem: {SOURCE_CHANNEL_ID}")
                except Exception as e:
                    logger.warning(f"Não foi possível entrar no canal {SOURCE_CHANNEL_ID} (pode já estar nele ou ser um canal privado). Erro: {e}")

                return # Conexão bem-sucedida
            except Exception as e:
                logger.error(f"Erro ao conectar ao Telegram: {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY_SECONDS) # Espera antes de tentar novamente
                else:
                    logger.critical("Falha crítica ao conectar ao Telegram após múltiplas tentativas. Encerrando.")
                    raise # Re-levanta a exceção se todas as tentativas falharem

    async def run_until_disconnected(self):
        """
        Mantém o cliente Telegram do listener rodando até ser desconectado.
        """
        if self.client.is_connected():
            await self.client.run_until_disconnected()
            logger.info("Cliente Telegram do listener desconectado.")
        else:
            logger.warning("Cliente Telegram do listener não estava conectado para ser executado.")

    async def disconnect(self):
        """
        Desconecta o cliente Telegram.
        """
        if self.client and self.client.is_connected():
            await self.client.disconnect()
            logger.info("Listener desconectado do Telegram.")

