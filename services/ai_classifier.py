# afiliado_bot/services/ai_classifier.py

from openai import OpenAI
import logging
import asyncio

# Importa as configurações da OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, IA_PROMPT_TEMPLATE, RETRY_ATTEMPTS, RETRY_DELAY_SECONDS

logger = logging.getLogger(__name__)

class AIClassifier:
    """
    Classe para interagir com a API da OpenAI para classificar a relevância de promoções.
    """
    def __init__(self):
        """
        Inicializa o cliente da OpenAI.
        """
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            logger.info("Cliente OpenAI inicializado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente OpenAI: {e}")
            self.client = None # Define como None para evitar chamadas futuras se a chave estiver inválida

    async def classify_relevance(self, promotion_text: str) -> str:
        """
        Classifica a relevância de um texto de promoção usando a OpenAI GPT-4.

        Args:
            promotion_text (str): O texto da promoção a ser classificado.

        Returns:
            str: "sim" se a promoção for relevante, "não" caso contrário.
                 Retorna "sim" por padrão em caso de falha da API.
        """
        if not self.client:
            logger.warning("Cliente OpenAI não está inicializado. Retornando 'sim' por padrão.")
            return "sim"

        prompt = IA_PROMPT_TEMPLATE.format(promotion_text=promotion_text)
        logger.debug(f"Enviando prompt para IA: {prompt[:200]}...")

        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "Você é um classificador de promoções."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=10 # Esperamos uma resposta curta ("sim" ou "não")
                )
                classification = response.choices[0].message.content.strip().lower()
                logger.info(f"IA classificou como: '{classification}' para a promoção: {promotion_text[:50]}...")
                return "sim" if "sim" in classification else "não"

            except Exception as e:
                logger.error(f"Erro ao chamar a API da OpenAI (tentativa {attempt + 1}/{RETRY_ATTEMPTS}): {e}")
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(RETRY_DELAY_SECONDS) # Espera antes de tentar novamente
                else:
                    logger.error("Falha ao classificar a promoção após múltiplas tentativas. Retornando 'sim' por padrão.")
                    return "sim" # Retorna "sim" por segurança em caso de falha persistente

