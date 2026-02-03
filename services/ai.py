import requests

from config import (
    MOCK_MODE,
    YC_IAM_TOKEN,
    YC_FOLDER_ID,
)
from ui.messages import API_URL


def generate_text(prompt: str) -> str:
    """
    Генерация текста через YandexGPT (HTTP API)
    """

    # 🧪 MOCK для локальной разработки
    if MOCK_MODE:
        return (
            "🧪 ТЕСТОВАЯ ГЕНЕРАЦИЯ\n\n"
            "🔥 Хук:\n"
            "«Пять минут в день, которые сделают тебя продуктивнее уже завтра»"
        )

    if not YC_IAM_TOKEN or not YC_FOLDER_ID:
        raise RuntimeError(
            "YC_IAM_TOKEN или YC_FOLDER_ID не заданы"
        )

    headers = {
        "Authorization": f"Bearer {YC_IAM_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "modelUri": f"gpt://{YC_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.9,
            "maxTokens": 300,
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты профессиональный сценарист для коротких видео."
            },
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print("❌ Ошибка запроса к YandexGPT:", e)
        raise

    result = response.json()
    return result["result"]["alternatives"][0]["message"]["text"].strip()
