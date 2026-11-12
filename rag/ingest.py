
import hashlib
from pathlib import Path

from knowledge_base.document_loader import extract_text
from knowledge_base.text_splitter import split_text
from rag.embedding import get_embedding
from rag.vector_store import add_chunks, get_collection


def ingest_document(file_path: str):
    """
    企业文档入库：
    计算文件指纹 -> 检查重复 -> 读取文档
    -> 切分文本 -> 生成向量 -> 保存数据库
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    # 第一步：计算文件 SHA-256 指纹
    print("1. 正在计算文件指纹...")

    file_bytes = path.read_bytes()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # 第二步：检查数据库是否已有相同文件
    print("2. 正在检查文件是否重复...")

    collection = get_collection()

    existing = collection.get(
        where={"file_hash": file_hash},
        limit=1
    )

    if existing["ids"]:
        print("发现重复文件，跳过入库！")

        return {
            "filename": path.name,
            "chunk_count": 0,
            "saved_count": 0,
            "duplicate": True
        }

    # 第三步：读取文档
    print("3. 正在读取文档...")

    text = extract_text(str(path))

    if not text.strip():
        raise ValueError("文档内容为空，无法入库")

    # 第四步：切分文本
    print("4. 正在切分文本...")

    chunks = split_text(
        text,
        chunk_size=500,
        chunk_overlap=100
    )

    print(f"文本块数量：{len(chunks)}")

    # 第五步：生成向量
    print("5. 正在生成文本向量...")

    embeddings = []

    for index, chunk in enumerate(chunks):
        vector = get_embedding(chunk)
        embeddings.append(vector)

        print(f"已完成：{index + 1}/{len(chunks)}")

    # 第六步：保存到数据库
    print("6. 正在保存到向量数据库...")

    ids = add_chunks(
        chunks,
        embeddings,
        source=path.name,
        file_hash=file_hash
    )

    return {
        "filename": path.name,
        "chunk_count": len(chunks),
        "saved_count": len(ids),
        "duplicate": False
    }
