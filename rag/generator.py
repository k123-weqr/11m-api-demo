
from api_client import chat_with_deepseek


def generate_answer(question: str, context_chunks: list):
    """
    根据用户问题和检索到的文档内容生成回答。
    """

    if not question.strip():
        raise ValueError("用户问题不能为空")

    if not context_chunks:
        return "知识库中没有找到相关资料，暂时无法回答。"

    # 整理检索到的文档内容
    context = "\n\n".join(
        item["text"] for item in context_chunks
    )

    # 构建发送给大模型的消息
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个企业知识库助手。"
                "请优先根据提供的知识库资料回答问题。"
                "如果资料中没有相关信息，请明确说明不知道，"
                "不要编造答案。"
            )
        },
        {
            "role": "user",
            "content": (
                f"知识库资料：\n{context}\n\n"
                f"用户问题：{question}\n\n"
                "请根据知识库资料回答。"
            )
        }
    ]

    # 调用原有的 DeepSeek API
    answer = chat_with_deepseek(messages)

    return answer
