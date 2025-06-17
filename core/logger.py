# afiliado_bot/core/logger.py

import logging
import sys

def setup_logging():
    """
    Configura o sistema de logging para o projeto.
    Mensagens INFO e superiores são enviadas para o console.
    """
    logging.basicConfig(
        level=logging.INFO, # Define o nível mínimo de log a ser processado
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Formato da mensagem de log
        handlers=[
            logging.StreamHandler(sys.stdout) # Envia logs para a saída padrão (console)
        ]
    )
    # Define o nível de log para a biblioteca telethon para evitar logs excessivos
    logging.getLogger('telethon').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)

