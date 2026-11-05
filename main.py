import streamlit as st
from api_client import chat_with_deepseek

st.set_page_config(page_title="DeepSeek 网页对话助手")
st.title("DeepSeek 网页对话助手")

# 精简系统提示，避免超大固定前缀疯狂堆缓存 token
SYSTEM_PROMPT = {
    "role": "system",
    "content": "你是一个简洁友好的对话助手，回答尽量精炼。"
}

if "msg_list" not in st.session_state:
    st.session_state.msg_list = [SYSTEM_PROMPT]

with st.sidebar:
    st.header("设置")
    temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    if st.button("导出对话为 Markdown"):
        lines = []
        for m in st.session_state.msg_list:
            if m["role"] == "system":
                continue
            lines.append(f"**{m['role']}**：\n{m['content']}\n\n")
        md_text = "\n".join(lines)
        st.download_button("下载", md_text, file_name="chat_log.md", mime="text/markdown")

    # 粗略本地统计
    all_text = "".join(m["content"] for m in st.session_state.msg_list)
    st.info(f"粗略预估总 Token：{len(all_text)}")

# 渲染历史
for msg in st.session_state.msg_list:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("在这里输入你的问题……")
if user_input:
    st.session_state.msg_list.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        reply = chat_with_deepseek(st.session_state.msg_list, temperature=temp)
    except Exception as e:
        reply = f"接口请求出错：{e}"

    st.session_state.msg_list.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)