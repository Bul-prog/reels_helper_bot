import requests
import os
from dotenv import load_dotenv

load_dotenv()

IAM_TOKEN = os.getenv("YC_IAM_TOKEN")
FOLDER_ID = os.getenv("YC_FOLDER_ID")

if not IAM_TOKEN or not FOLDER_ID:
    raise RuntimeError("YC_IAM_TOKEN or YC_FOLDER_ID is not set")

url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

headers = {
    "Authorization": f"Bearer {IAM_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0.9,
        "maxTokens": 200
    },
    "messages": [
        {
            "role": "system",
            "text": "Ты профессиональный сценарист для коротких видео."
        },
        {
            "role": "user",
            "text": "Придумай сильный хук для видео про личную продуктивность."
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

# 👇 если снова ошибка — увидим точное сообщение от Яндекса
print("STATUS:", response.status_code)
print("RAW RESPONSE:", response.text)

response.raise_for_status()

result = response.json()
print("\n=== RESULT ===\n")
print(result["result"]["alternatives"][0]["message"]["text"])
