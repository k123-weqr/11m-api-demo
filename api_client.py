import requests
from utils import load_api_key

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def chat_with_deepseek(messages: list, temperature: float = 0.7):
    api_key = load_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature
    }
    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"接口请求出错：{str(e)}"