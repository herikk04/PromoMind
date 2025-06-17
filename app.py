import asyncio
from services.telegram_listener import start_listener
from core.logger import setup_logger

logger = setup_logger()

if __name__ == "__main__":
    try:
        logger.info("Iniciando bot de monitoramento de promoções...")
        asyncio.run(start_listener())
    except KeyboardInterrupt:
        logger.info("Encerrando execução do bot...")