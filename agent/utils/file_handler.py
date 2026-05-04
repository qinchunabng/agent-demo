import hashlib
import os.path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from agent.utils.logger_handler import logger


# 计算文件的MD5哈希值
def get_file_md5_hex(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]File {filepath} doesn't exist")
        return None
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]File {filepath} isn't a file")
        return None

    md5_obj = hashlib.md5()

    chunk_size = 4096
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"[md5计算] 计算文件 {filepath} 的MD5哈希值时出错 Error: {str(e)}")
        return None

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type] {path} is not a directory")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return tuple(files)

def pdf_loader(filepath: str, passwd: str = None) -> list[Document]:
    return PyPDFLoader(filepath, password=passwd).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding='utf-8').load()