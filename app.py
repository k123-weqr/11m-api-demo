
import streamlit as st
from pathlib import Path

from rag.ingest import ingest_document
from rag.rag_pipeline import ask_knowledge_base


# ===================== 项目目录 =====================

PROJECT_ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ===================== 页面设置 =====================

st.set_page_config(
    page_title="企业知识库助手",
    page_icon="📚",
    layout="centered"
)

st.title("📚 企业知识库助手")
st.write("上传企业文档，让 AI 学习你的企业资料。")


# ===================== 第一部分：文档上传 =====================

st.header("第一步：上传企业文档")

uploaded_file = st.file_uploader(
    "请选择需要上传的文件",
    type=["txt", "pdf", "docx"]
)

if uploaded_file is not None:

    st.success(f"已选择文件：{uploaded_file.name}")

    if st.button("开始上传并入库", type="primary"):

        try:
            file_path = UPLOAD_DIR / Path(uploaded_file.name).name

            # 保存上传文件
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # 执行文档入库
            with st.spinner("正在处理文档，请稍候..."):
                result = ingest_document(str(file_path))

            if result["duplicate"]:
                st.warning("检测到重复文档，本次跳过入库！")
            else:
                st.success("文档入库成功！")

            st.write("文件名称：", result["filename"])
            st.write("文本块数量：", result["chunk_count"])
            st.write("成功保存数量：", result["saved_count"])

        except Exception as e:
            st.error(f"文档处理失败：{e}")


st.divider()


# ===================== 第二部分：AI 知识库问答 =====================

st.header("第二步：AI 知识库问答")

st.write("你可以向 AI 提问，它会根据已经上传的企业文档回答。")


# 初始化聊天历史
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# 展示历史对话
for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # 展示检索到的资料来源
        if message.get("sources"):
            with st.expander("查看知识库参考资料"):

                for index, item in enumerate(message["sources"]):
                    st.write(f"资料 {index + 1}")
                    st.write("来源文件：", item["metadata"]["source"])
                    st.write("相关内容：", item["text"])
                    st.write("距离值：", item["distance"])


# 用户输入问题
question = st.chat_input("请输入你想了解的问题...")


if question:

    # 展示用户问题
    st.session_state.chat_history.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # 调用 RAG 完整问答流程
    with st.chat_message("assistant"):

        with st.spinner("正在检索企业资料并生成回答..."):

            try:
                result = ask_knowledge_base(question)

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                # 展示本次回答的参考资料
                if sources:
                    with st.expander("查看知识库参考资料"):

                        for index, item in enumerate(sources):
                            st.write(f"资料 {index + 1}")
                            st.write("来源文件：", item["metadata"]["source"])
                            st.write("相关内容：", item["text"])
                            st.write("距离值：", item["distance"])

                # 保存 AI 回答
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:
                st.error(f"问答失败：{e}")


st.divider()

st.caption("当前支持 TXT、PDF、DOCX 文档上传及知识库问答。")
