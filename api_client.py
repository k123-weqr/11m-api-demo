import requests
from utils import load_api_key, truncate_messages

API_URL = "https://api.deepseek.com/v1/chat/completions"
# 想省钱就改成 "deepseek-flash"，原来的是 "deepseek-chat"
MODEL_NAME = "deepseek-flash"


def chat_with_deepseek(messages, temperature=0.7):
    key = load_api_key()
    # 截断！传给接口之前先切
    messages = truncate_messages(messages, max_rounds=6)

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }

    resp = requests.post(
    API_URL,
    headers=headers,
    json=payload,
    timeout=60
)

    if resp.status_code != 200:
        err_text = resp.text
        raise RuntimeError(f"{resp.status_code} Client Error: {err_text}")

    data = resp.json()
    usage = data.get("usage", {})
    prompt_hit = usage.get("prompt_cache_hit_tokens", 0)
    prompt_miss = usage.get("prompt_cache_miss_tokens", 0)
    comp = usage.get("completion_tokens", 0)

    # 简单估算价格（参考官方公开单价，仅用来心里有数）
    # flash：缓存命中很便宜，这里只是粗略日志，不作为结算
    est_cost = (
        prompt_hit * 0.0000001
        + prompt_miss * 0.000001
        + comp * 0.000004
    )

    print("===== 本次调用开销日志 =====")
    print(f"缓存命中输入：{prompt_hit}")
    print(f"新输入：{prompt_miss}")
    print(f"输出 token：{comp}")
    print(f"预估花费：≈ {est_cost:.6f} 元")
    print("============================")

    return data["choices"][0]["message"]["content"]