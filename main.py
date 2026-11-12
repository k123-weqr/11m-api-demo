import sys
import os
import re

sys.stdout.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# ===================== 加载 .env（老版本兼容写法） =====================
BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_file)

api_key = os.getenv("DEEPSEEK_API_KEY")

# 调试打印

if api_key:
    print("密钥长度：", len(api_key))
else:
    print("密钥：None，没有读到！")

if not api_key:
    st.error("❌ 没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件！")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ===================== 页面基础设置 =====================
st.set_page_config(page_title="DeepSeek 流式对话", layout="wide")
st.title("DeepSeek 流式对话")

# ===================== 侧边栏 =====================
with st.sidebar:
    st.header("设置面板")
    model_name = st.selectbox(
        "选择模型",
        ["deepseek-flash", "deepseek-chat"]
    )
    temperature = st.slider("temperature（温度）", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("单次最大输出 token", 100, 4000, 1000, 100)

    st.divider()
    st.markdown("### Token 粗略估算（本地估算，仅供参考）")
    if "total_input_tokens" not in st.session_state:
        st.session_state.total_input_tokens = 0
    if "total_output_tokens" not in st.session_state:
        st.session_state.total_output_tokens = 0

    st.write(f"累计输入估算：{st.session_state.total_input_tokens}")
    st.write(f"累计输出估算：{st.session_state.total_output_tokens}")

    if st.button("清空对话 & 重置统计"):
        st.session_state.messages = []
        st.session_state.total_input_tokens = 0
        st.session_state.total_output_tokens = 0
        st.rerun()

# 简易估算函数（不用 tiktoken）
def estimate_tokens(text: str) -> int:
    return len(text) // 4

# ===================== 对话记忆 =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===================== 用户输入 =====================
user_input = st.chat_input("在这里输入你的问题……")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 估算输入 token
    st.session_state.total_input_tokens += estimate_tokens(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""

        stream = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                piece = chunk.choices[0].delta.content
                response_text += piece
                placeholder.markdown(response_text)

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.session_state.total_output_tokens += estimate_tokens(response_text)