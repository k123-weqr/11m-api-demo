
import chromadb
from pathlib import Path
from uuid import uuid4


# 获取项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 数据库保存位置
DB_PATH = PROJECT_ROOT / "chroma_db"


def get_collection():
    """
    创建或获取 ChromaDB 知识集合。
    """

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name="company_knowledge",
        metadata={"hnsw:space": "cosine"}
    )

    return collection



def add_chunks(chunks, embeddings, source="unknown", file_hash=None):
    if len(chunks) != len(embeddings):
        raise ValueError("文本块数量和向量数量不一致")

    if not chunks:
        return []

    collection = get_collection()

    ids = [str(uuid4()) for _ in chunks]

    metadatas = []

    for _ in chunks:
        metadata = {"source": source}

        if file_hash:
            metadata["file_hash"] = file_hash

        metadatas.append(metadata)

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return ids



def search_chunks(query_embedding, top_k=3):
    """
    根据问题向量，检索最相关的文本块。
    """

    collection = get_collection()

    total = collection.count()

    if total == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total),
        include=["documents", "metadatas", "distances"]
    )

    matched_chunks = []

    for i in range(len(results["ids"][0])):
        matched_chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return matched_chunks
