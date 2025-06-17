import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def is_relevant(text):
    prompt = f"""
    Avalie a seguinte promoção e responda apenas "SIM" ou "NÃO".

    Texto:
    {text}

    A promoção é relevante?"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em promoções e e-commerce."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip().upper()
        return answer == "SIM"
    except Exception as e:
        return False