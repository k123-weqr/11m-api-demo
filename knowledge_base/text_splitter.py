
def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    """将长文本切分成带有上下文重叠的小文本块。"""

    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")

    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap 不能小于 0")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap 必须小于 chunk_size")

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    boundaries = ["\n", "。", "！", "？", "；"]

    while start < text_length:

        end = min(start + chunk_size, text_length)

        # 尽量在自然语句边界结束
        if end < text_length:
            search_start = start + chunk_size // 2

            positions = [
                text.rfind(mark, search_start, end)
                for mark in boundaries
            ]

            boundary = max(positions)

            if boundary != -1:
                end = boundary + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        # 计算下一块的理想起点
        next_start = max(start + 1, end - chunk_overlap)

        # 如果起点落在句子中间，尝试向后移动到句子边界
        search_end = min(next_start + 20, end)

        positions = [
            text.find(mark, next_start, search_end)
            for mark in boundaries
        ]

        positions = [p for p in positions if p != -1]

        if positions:
            next_start = min(positions) + 1

        start = next_start

    return chunks
