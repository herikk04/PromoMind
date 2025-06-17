# 🧠 PromoMind um Bot de Monitoramento de Promoções no Telegram

> 📌 **Nota sobre esta branch (`PromoMind`):**  
> Esta branch é uma reestruturação mais sofisticada e detalhada da `main`.  
> Enquanto a `main` serviu como um esqueleto inicial do projeto, esta versão foi redesenhada com foco em clareza, organização e completude.  
> Os comentários no código foram elaborados com o auxílio de inteligência artificial para melhorar a legibilidade e facilitar o entendimento técnico.

Este projeto é um bot Python robusto e modular projetado para monitorar promoções em um canal específico do Telegram, filtrar links relevantes, gerar links de afiliado automaticamente usando inteligência artificial (OpenAI GPT-4) para classificação e, finalmente, republicar as promoções aprovadas em seu próprio canal Telegram.

Funcionalidades
Monitoramento em Tempo Real: Escuta novas mensagens em um canal Telegram configurável.

Extração e Validação de Links: Extrai URLs de mensagens e verifica se pertencem a domínios permitidos (Amazon, AliExpress, Mercado Livre, Magazine Luiza, Shopee).

Geração de Links de Afiliado: Converte URLs válidas em links de afiliado com base em configurações personalizáveis por domínio.

Classificação por IA: Utiliza a API da OpenAI (GPT-4) para determinar a relevância da promoção a partir do texto da mensagem.

Prevenção de Duplicidade: Armazena links já publicados em um banco de dados SQLite para evitar republicações.

Publicação Automatizada: Posta promoções aprovadas no canal de destino com o link de afiliado já incorporado.

Notificações ao Administrador: Envia mensagens privadas para o administrador para promoções rejeitadas pela IA ou em caso de erros.

Logging Detalhado: Geração de logs para monitorar o funcionamento, erros e eventos do bot.

Configuração Externa: Todas as variáveis configuráveis (credenciais, IDs de canais, chaves de API, etc.) são gerenciadas via um arquivo settings.py e variáveis de ambiente.

Arquitetura Modular: Projeto organizado em módulos e pacotes para facilitar a manutenção e escalabilidade.

Resiliência: Tratamento de erros e mecanismos de reconexão/retry para operação 24/7.

```bash
Estrutura do Projeto

afiliado_bot/
│
├── app.py                  # Ponto de entrada principal para iniciar o bot
├── config/
│   └── settings.py         # Arquivo de configuração com variáveis de ambiente
├── core/
│   └── logger.py           # Configuração do sistema de logging
├── domain/
│   ├── link_model.py       # Modelo de dados para links
│   └── link_parser.py      # Lógica para extração e construção de links de afiliado
├── services/
│   ├── ai_classifier.py    # Integração com OpenAI para classificação de promoções
│   ├── database.py         # Gerenciamento do banco de dados SQLite
│   ├── notifier.py         # Envio de notificações para o administrador
│   ├── telegram_listener.py# Componente para escutar mensagens no canal de origem
│   └── telegram_sender.py  # Componente para enviar mensagens para o canal de destino
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```
Instalação
Clone o repositório:
```bash
git clone https://github.com/herikk04/PromoMind.git
cd PromoMind
```
Crie e ative um ambiente virtual (recomendado):

python -m venv venv
# No Windows:
```bash
.\venv\Scripts\activate
```

# No macOS/Linux:

```bash
source venv/bin/activate
```

# Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração
Edite o arquivo `config/settings.py` com suas credenciais e IDs. Alternativamente, você pode definir essas variáveis como variáveis de ambiente no seu sistema.

Variáveis Obrigatórias:
- `TELEGRAM_API_ID`: Obtido em my.telegram.org.

- `TELEGRAM_API_HASH`: Obtido em my.telegram.org.

- `TELEGRAM_BOT_TOKEN`: Obtido do BotFather no Telegram (crie um novo bot e copie o token).

- `SOURCE_CHANNEL_ID` O ID numérico do canal Telegram de onde o bot vai monitorar as promoções. Para obter o ID de um canal, você pode encaminhar uma mensagem do canal para o bot @RawDataBot no Telegram. O ID será um número negativo (ex: -1001234567890).

- `DESTINATION_CHANNEL_ID`: O ID numérico do seu canal Telegram onde o bot vai postar as promoções aprovadas. Certifique-se de que seu bot é um administrador neste canal com permissões para enviar mensagens.

- `ADMIN_CHAT_ID`: Seu ID de chat pessoal no Telegram para receber notificações de promoções rejeitadas ou erros. Você pode enviar uma mensagem para o @RawDataBot e copiar seu ID (from -> id).

- `OPENAI_API_KEY`: Sua chave de API da OpenAI, obtida em platform.openai.com.

- `AFFILIATE_CONFIG`: Um dicionário Python dentro de `settings.py` que mapeia os domínios para seus respectivos IDs de afiliado e parâmetros de rastreamento. Preencha com suas informações de afiliado reais.

Exemplo de `config/settings.py` (com placeholders):

# config/settings.py
```python
import os

API_ID = int(os.getenv("TELEGRAM_API_ID", "SEU_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "SEU_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_BOT_TOKEN")

SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID", -1234567890))
DESTINATION_CHANNEL_ID = int(os.getenv("DESTINATION_CHANNEL_ID", -1234567891))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 123456789))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_OPENAI")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

IA_PROMPT_TEMPLATE = """
# ... (conteúdo do prompt) ...
"""

AFFILIATE_CONFIG = {
    "amazon.com.br": {
        "affiliate_id": os.getenv("AFFILIATE_ID_AMAZON", "seu_id_amazon-20"),
        "param": "tag"
    },
    "aliexpress.com": {
        "affiliate_id": os.getenv("AFFILIATE_ID_ALIEXPRESS", "seu_id_aliexpress"),
        "param": "aff_platform",
        "extra_params": {"albpt": "test"}
    },
    # ... outros domínios
}

DATABASE_NAME = os.getenv("DATABASE_NAME", "posted_links.db")
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", 3))
RETRY_DELAY_SECONDS = int(os.getenv("RETRY_DELAY_SECONDS", 5))
```
#
# Execução
Após configurar o `settings.py` ou as variáveis de ambiente, você pode iniciar o bot:
```bash
python app.py
```

Na primeira execução, o Telethon pode solicitar seu número de telefone para autenticação. Siga as instruções no terminal.

Para manter o bot funcionando 24/7, considere usar ferramentas como systemd, Supervisor ou Docker para gerenciar o processo em um servidor.
#
# Tratamento de Erros e Resiliência
O bot foi projetado com mecanismos de retry para falhas de conexão com o Telegram ou chamadas à API da OpenAI. Logs detalhados são gerados para ajudar no diagnóstico de problemas.

# Contribuição
Sinta-se à vontade para contribuir com melhorias, testes ou novas funcionalidades. Abra uma issue ou pull request no repositório.

# Licença
Este projeto está sob a licença MIT.