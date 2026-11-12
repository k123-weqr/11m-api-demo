import os
from dotenv import load_dotenv

load_dotenv()

def load_api_key():
    # 优先从系统环境变量或本地 .env 读取
    key = os.getenv("DEEPSEEK_API_KEY")

    # 如果没有读取到，再尝试从 Streamlit Cloud Secrets 读取
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("DEEPSEEK_API_KEY")
        except Exception:
            key = None

    if not key:
        raise ValueError(
            "没有读取到 DEEPSEEK_API_KEY，请检查环境变量或 Streamlit Secrets"
        )

    return key

def truncate_messages(messages, max_rounds=6):
    """只保留最近 max_rounds 轮对话，系统提示词保留在最前面"""
    system_msg = None
    rest = []
    for m in messages:
        if m["role"] == "system":
            system_msg = m
        else:
            rest.append(m)

    # 保留最新 N 轮
    rest = rest[-max_rounds * 2:]
    out = []
    if system_msg:
        out.append(system_msg)
    out.extend(rest)
    return out