# afiliado_bot/domain/link_parser.py

import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import logging

logger = logging.getLogger(__name__)

class LinkParser:
    """
    Classe responsável por extrair URLs de mensagens, validar domínios
    e construir links de afiliado.
    """
    def __init__(self, affiliate_config: dict):
        """
        Inicializa o LinkParser com as configurações de afiliado.

        Args:
            affiliate_config (dict): Dicionário com configurações de afiliado por domínio.
        """
        self.affiliate_config = affiliate_config
        self.allowed_domains = list(affiliate_config.keys())
        logger.info(f"Domínios permitidos para links de afiliado: {self.allowed_domains}")

    def extract_and_validate_links(self, text: str) -> list[str]:
        """
        Extrai URLs de um texto e filtra apenas aquelas que pertencem aos domínios permitidos.

        Args:
            text (str): O texto da mensagem de onde extrair os links.

        Returns:
            list[str]: Uma lista de URLs válidas e permitidas.
        """
        # Regex para encontrar URLs no texto
        # Adiciona suporte para URLs que podem não ter http/https no início, mas que começam com www.
        url_pattern = r'https?://[^\s]+|www\.[^\s]+'
        found_urls = re.findall(url_pattern, text)
        valid_urls = []

        for url in found_urls:
            # Adiciona https:// se a URL começar apenas com www.
            if url.startswith("www."):
                url = "https://" + url

            try:
                parsed_url = urlparse(url)
                # Verifica se o netloc (domínio) é um dos domínios permitidos
                # Usa .endswith para pegar subdomínios também (ex: shop.amazon.com.br)
                if any(parsed_url.netloc.endswith(domain) for domain in self.allowed_domains):
                    valid_urls.append(url)
                    logger.debug(f"Link válido encontrado: {url}")
                else:
                    logger.debug(f"Link inválido (domínio não permitido): {url}")
            except Exception as e:
                logger.warning(f"Erro ao parsear URL '{url}': {e}")
        return valid_urls

    def generate_affiliate_link(self, original_url: str) -> str | None:
        """
        Gera um link de afiliado para a URL original, se o domínio for configurado.

        Args:
            original_url (str): A URL original da promoção.

        Returns:
            str | None: O link de afiliado gerado ou None se não for possível.
        """
        try:
            parsed_url = urlparse(original_url)
            domain = parsed_url.netloc

            # Encontra a configuração de afiliado correspondente
            config = None
            for allowed_domain, aff_config in self.affiliate_config.items():
                if domain.endswith(allowed_domain):
                    config = aff_config
                    break

            if not config:
                logger.warning(f"Domínio '{domain}' não tem configuração de afiliado.")
                return None

            affiliate_id = config.get("affiliate_id")
            param_name = config.get("param")
            extra_params = config.get("extra_params", {})

            if not affiliate_id or not param_name:
                logger.warning(f"Configuração de afiliado incompleta para o domínio '{domain}'.")
                return None

            # Parseia os parâmetros da URL original
            query_params = parse_qs(parsed_url.query)

            # Adiciona ou atualiza o parâmetro de afiliado
            query_params[param_name] = [affiliate_id]

            # Adiciona parâmetros extras
            for key, value in extra_params.items():
                query_params[key] = [value]

            # Constrói a nova string de query
            new_query = urlencode(query_params, doseq=True)

            # Reconstrói a URL com os novos parâmetros
            affiliate_url = urlunparse(parsed_url._replace(query=new_query))

            logger.info(f"Link de afiliado gerado: {affiliate_url} para {original_url}")
            return affiliate_url

        except Exception as e:
            logger.error(f"Erro ao gerar link de afiliado para {original_url}: {e}")
            return None

