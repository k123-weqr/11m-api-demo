
from pathlib import Path
from io import BytesIO

from pypdf import PdfReader
from docx import Document


def read_file_bytes(file):
    """
    将上传文件或本地文件统一转换成 bytes。
    """

    if isinstance(file, (str, Path)):
        return Path(file).read_bytes()

    if hasattr(file, "getvalue"):
        return file.getvalue()

    if hasattr(file, "read"):
        file.seek(0)
        return file.read()

    raise ValueError("不支持的文件类型")


def load_txt(data):
    """读取 TXT 文件"""

    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("gb18030")


def load_pdf(data):
    """读取 PDF 文件"""

    reader = PdfReader(BytesIO(data))

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)

    return "\n".join(pages)


def load_docx(data):
    """读取 Word 文件"""

    document = Document(BytesIO(data))

    contents = []

    # 读取普通段落
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            contents.append(paragraph.text)

    # 读取表格
    for table in document.tables:
        for row in table.rows:
            row_text = " | ".join(
                cell.text.strip() for cell in row.cells
            )
            if row_text.strip():
                contents.append(row_text)

    return "\n".join(contents)


def extract_text(file):
    """
    根据文件后缀自动选择读取方式。
    支持 PDF、TXT、DOCX。
    """

    filename = getattr(file, "name", None)

    if filename is None:
        filename = Path(file).name

    suffix = Path(filename).suffix.lower()

    data = read_file_bytes(file)

    if suffix == ".txt":
        text = load_txt(data)

    elif suffix == ".pdf":
        text = load_pdf(data)

    elif suffix == ".docx":
        text = load_docx(data)

    else:
        raise ValueError(f"暂不支持该文件格式：{suffix}")

    if not text.strip():
        raise ValueError("没有从文件中提取到有效文字")

    return text
