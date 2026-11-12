
import os
import requests
from dotenv import load_dotenv

# 加载本地 .env 文件
load_dotenv()

# API 地址
API_URL = "https://api.siliconflow.cn/v1/embeddings"

# 使用的向量模型
MODEL_NAME = "BAAI/bge-m3"


def get_api_key():
    # 优先读取本地环境变量或 .env
    key = os.getenv("SILICONFLOW_API_KEY")

    # 如果没有，再读取 Streamlit Cloud Secrets
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("SILICONFLOW_API_KEY")
        except Exception:
            key = None

    return key


def get_embedding(text: str):
    """
    将一段文本转换成向量。
    """

    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")

    if not text.strip():
        raise ValueError("输入文本不能为空")

    # 获取 API Key
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "没有读取到 SILICONFLOW_API_KEY，请检查环境变量或 Streamlit Secrets"
        )

    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 请求数据
    payload = {
        "model": MODEL_NAME,
        "input": text,
        "encoding_format": "float"
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        embedding = result["data"][0]["embedding"]

        return embedding

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Embedding API 请求失败：{e}") from e

    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError("Embedding API 返回的数据格式不正确") from e
