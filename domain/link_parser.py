import re
from urllib.parse import urlparse, urlunparse
from config.settings import AFILIADOS
from domain.link_model import LinkInfo

VALID_DOMAINS = AFILIADOS.keys()

URL_REGEX = r"https?://[\w./?=&%-]+"

def extract_links(text):
    return re.findall(URL_REGEX, text)

def build_affiliate_link(url):
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    if domain not in VALID_DOMAINS:
        return None
    params = AFILIADOS[domain]
    new_url = urlunparse(parsed._replace(query=params.strip("?")))
    return LinkInfo(original_url=url, domain=domain, afiliado_url=new_url)