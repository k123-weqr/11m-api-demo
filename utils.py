import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件")
    return key


def export_chat_markdown(messages: list) -> str:
    md = "# 对话记录\n\n"
    for msg in messages:
        role_label = "用户" if msg["role"] == "user" else "助手"
        md += f"**{role_label}**：\n{msg['content']}\n\n"
    return md


def estimate_token_count(text: str) -> int:
    # 简易估算：英文约 4 字符一个 token，中文大约 1 个字一个 token
    return len(text)