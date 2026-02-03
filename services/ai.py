import requests

from config import (
    MOCK_MODE,
    YC_IAM_TOKEN,
    YC_FOLDER_ID,
    YC_OAUTH_TOKEN,
)
from ui.messages import API_URL
import time

_IAM_CACHE = {
    "token": None,
    "expires_at": 0,
}

def get_iam_token() -> str:
    now = time.time()

    if _IAM_CACHE["token"] and now < _IAM_CACHE["expires_at"]:
        return _IAM_CACHE["token"]

    resp = requests.post(
        "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        json={"yandexPassportOauthToken": YC_OAUTH_TOKEN},
        timeout=10
    )
    resp.raise_for_status()

    iam_token = resp.json()["iamToken"]

    # IAM живёт ~12 часов, берём с запасом
    _IAM_CACHE["token"] = iam_token
    _IAM_CACHE["expires_at"] = now + 60 * 60 * 10  # 10 часов

    return iam_token


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

    if not YC_OAUTH_TOKEN or not YC_FOLDER_ID:
        raise RuntimeError("YC_OAUTH_TOKEN или YC_FOLDER_ID не заданы")

    iam_token = get_iam_token()

    headers = {
        "Authorization": f"Bearer {iam_token}",
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
