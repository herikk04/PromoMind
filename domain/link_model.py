# afiliado_bot/domain/link_model.py

from dataclasses import dataclass

@dataclass
class Link:
    """
    Modelo de dados para representar um link.
    """
    original_url: str
    domain: str
    affiliate_id: str = None
    affiliate_url: str = None

