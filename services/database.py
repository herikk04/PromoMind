# afiliado_bot/services/database.py

import aiosqlite
import logging

# Importa o nome do banco de dados das configurações
from config.settings import DATABASE_NAME

logger = logging.getLogger(__name__)

class Database:
    """
    Classe para gerenciar as operações do banco de dados SQLite.
    Armazena URLs de links já postados para evitar duplicidade.
    """
    def __init__(self):
        """
        Inicializa a classe Database com o nome do arquivo do banco de dados.
        """
        self.db_name = DATABASE_NAME
        logger.info(f"Banco de dados configurado: {self.db_name}")

    async def init_db(self):
        """
        Inicializa o banco de dados e cria a tabela 'posted_links' se ela não existir.
        A tabela armazena a URL original do link e a data/hora em que foi postado.
        """
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS posted_links (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_url TEXT UNIQUE NOT NULL,
                        posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.commit()
            logger.info("Tabela 'posted_links' verificada/criada no banco de dados.")
        except Exception as e:
            logger.error(f"Erro ao inicializar o banco de dados: {e}")

    async def add_posted_link(self, original_url: str):
        """
        Adiciona uma URL ao banco de dados, marcando-a como já postada.

        Args:
            original_url (str): A URL original a ser adicionada.
        """
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("INSERT INTO posted_links (original_url) VALUES (?)", (original_url,))
                await db.commit()
            logger.info(f"Link '{original_url}' adicionado ao banco de dados.")
        except aiosqlite.IntegrityError:
            logger.warning(f"Tentativa de adicionar link duplicado: '{original_url}'.")
        except Exception as e:
            logger.error(f"Erro ao adicionar link '{original_url}' ao banco de dados: {e}")

    async def is_link_posted(self, original_url: str) -> bool:
        """
        Verifica se uma URL já foi postada anteriormente (existe no banco de dados).

        Args:
            original_url (str): A URL a ser verificada.

        Returns:
            bool: True se a URL já foi postada, False caso contrário.
        """
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT 1 FROM posted_links WHERE original_url = ?", (original_url,))
                result = await cursor.fetchone()
                return result is not None
        except Exception as e:
            logger.error(f"Erro ao verificar se o link '{original_url}' foi postado: {e}")
            return False # Em caso de erro, assumimos que não foi postado para evitar bloqueio

