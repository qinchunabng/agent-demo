from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    def __init__(self, embedding):
        """
        向量存储服务
        :param embedding: 向量嵌入模型
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        """
        获取向量检索器
        :return:
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model = "text-embedding-v4")
    retriever = VectorStoreService(embedding).get_retriever()

    res = retriever.invoke(input="我体重180斤，推荐尺码")
    print(res)
