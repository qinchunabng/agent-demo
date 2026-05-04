import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.utils.config_handler import chroma_conf
from agent.model.factory import embed_model, chat_model
from agent.utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from agent.utils.logger_handler import logger
from agent.utils.path_tool import get_abs_path


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf['collection_name'],
            embedding_function=embed_model,
            persist_directory=chroma_conf['persist_directory'],
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf['chunk_size'],
            chunk_overlap=chroma_conf['chunk_overlap'],
            separators=chroma_conf['separators'],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={
            "k": chroma_conf['k'],
        })

    def load_documents(self):
        """
        从数据文件夹中读取数据库文件，转为向量存入向量库
        :return:
        """
        def check_md5(md5_for_check: str):
            if not os.path.exists(chroma_conf['md5_hex_store']):
                open(chroma_conf['md5_hex_store'], 'w', encoding='utf-8').close()
                return False

            with open(chroma_conf['md5_hex_store'], 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if line.strip() == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_check: str):
            with open(chroma_conf['md5_hex_store'], 'a', encoding='utf-8') as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            try:
                if read_path.lower().endswith(".txt"):
                    return txt_loader(read_path)
                elif read_path.lower().endswith(".pdf"):
                    return pdf_loader(read_path)
                else:
                    logger.warning(f"[get_file_documents] 不支持的文件类型: {read_path}")
                    return []
            except Exception as e:
                logger.error(f"[get_file_documents] 加载文件 {read_path} 时出错: {str(e)}")
                return []

        allowed_files_path:list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5(md5_hex):
                logger.info(f"[load_documents] {path} is already in the vector store")
                continue

            try:
                documents:list[Document] = get_file_documents(path)
                if not documents:
                    logger.warning(f"[load_documents] {path} is not a valid document file")
                    continue

                split_documents:list[Document] = self.splitter.split_documents(documents)

                if not split_documents:
                    logger.warning(f"[load_documents] {os.path} is not a valid document file")
                    continue

                #将内容存入向量库
                self.vector_store.add_documents(split_documents)
                #将文件的md5哈希值存入文件
                save_md5_hex(md5_hex)
                logger.info(f"[load_documents] {path} is loaded to the vector store")
            except Exception as e:
                logger.error(f"[load_documents] {path} is loaded to the vector store Error: {str(e)}")
                continue

if __name__ == '__main__':
    store = VectorStoreService()
    store.load_documents()

    retriever = store.get_retriever()
    res = retriever.invoke("迷路")

    for r in res:
        print(r.page_content)
        print("-" * 20)