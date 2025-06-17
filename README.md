# Bot de Promoções com Telegram, IA e Links de Afiliado

## Visão geral
Este bot monitora um canal do Telegram, filtra promoções com IA, gera links de afiliado e publica em outro canal.

## Instalação
```bash
git clone https://github.com/seuusuario/afiliado_bot.git
cd afiliado_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuração
Crie um arquivo `.env` ou defina variáveis de ambiente com:
- API_ID
- API_HASH
- BOT_TOKEN
- OPENAI_API_KEY
- CHANNEL_ORIGEM
- CHANNEL_DESTINO
- ADMIN_CHAT_ID

## Execução
```bash
python app.py
```

## Estrutura
- `config/`: configurações gerais
- `core/`: utilitários centrais como logger
- `domain/`: lógica de domínio (parsing de links)
- `services/`: funcionalidades (IA, Telegram, DB)

## Licença
MIT
