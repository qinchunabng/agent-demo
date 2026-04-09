from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)

loader = CSVLoader(
    "./data/info.csv",
    encoding="utf-8",
    source_column="source"
)


documents = loader.load()
# print(documents[0])

#向量存储的增删改查
vector_store.add_documents(
    documents=documents, #被添加的文档
    ids=[f"doc_{i}" for i in range(len(documents))] #文档的id
)

#向量删除
vector_store.delete(["doc_0"])

#检索
results = vector_store.similarity_search(
    query="Python是不是简单易学", #查询的文本
    # 筛选出与查询最相似的文档数量
    k=3,
)

for result in results:
    print(result)