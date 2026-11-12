
from rag.embedding import get_embedding
from rag.vector_store import search_chunks
from rag.generator import generate_answer


def ask_knowledge_base(question: str, top_k: int = 3):
    """
    企业知识库完整问答流程：
    1. 将问题转换成向量
    2. 从向量数据库检索相关资料
    3. 将资料交给大模型生成答案
    """

    if not isinstance(question, str):
        raise TypeError("问题必须是字符串")

    if not question.strip():
        raise ValueError("问题不能为空")

    # 第一步：问题向量化
    query_embedding = get_embedding(question)

    # 第二步：检索相关资料
    context_chunks = search_chunks(
        query_embedding,
        top_k=top_k
    )

    # 第三步：生成回答
    answer = generate_answer(
        question,
        context_chunks
    )

    return {
        "question": question,
        "answer": answer,
        "sources": context_chunks
    }
