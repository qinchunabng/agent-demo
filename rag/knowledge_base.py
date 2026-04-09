"""
知识库
"""
import hashlib
import os.path
from datetime import datetime

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config_data as config

def check_md5(md5_str: str):
    """
    检查传入md5字符串是否已经被处理过
    :return:
    """
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        with open(config.md5_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line == md5_str:
                    return True

    return False

def save_md5(md5_str: str):
    """
    将传入的MD5字符串，记录到文件内保存
    :return:
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str):
    """
    将传入的字符串转为md5字符串
    :return:
    """
    str_bytes = input_str.encode('utf-8') #得到字符串字节数组
    md5_obj = hashlib.md5() #得到md5对象
    md5_obj.update(str_bytes) #更新内容
    return md5_obj.hexdigest() #得到md5十六进制字符串

class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件夹不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory=config.persist_directory,
        ) # 向量存储的实例 Chroma向量库实例
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        ) #文本分割器对象

    def upload_by_str(self, data: str, filename):
        """
        将传入的字符串，进行向量化，存入向量数据库
        :param data:
        :param filename:
        :return:
        """
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已存在知识库"

        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str] = self.splitter.split_text(data)
            print("分割后的文档数量:", len(knowledge_chunks))
        else:
            knowledge_chunks:list[str] = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )
        save_md5(md5_hex)
        return "[成功]知识库更新成功"


if __name__ == '__main__':
    # r1 = get_string_md5("周杰伦")
    # r2 = get_string_md5("周杰伦")
    # r3 = get_string_md5("周杰伦2")
    #
    # print(r1)
    # print(r2)
    # print(r3)
    #
    # print(check_md5(r1))

    knowledge_base_service = KnowledgeBaseService()

    with open("../data/尺码推荐.txt", 'r', encoding='utf-8') as f:
        content = f.read()
        knowledge_base_service.upload_by_str(content, "黑马程序员")