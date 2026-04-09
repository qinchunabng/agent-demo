from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("./data/Python基础语法.txt", encoding="utf-8")

documents = loader.load()

# print(documents)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # 分段的最大字符数
    chunk_overlap=50, # 分段之间的重叠字符数
    separators=["\n\n", "\n",".","。","?","？","!","！"," ",""], # 分隔符
    length_function=len, # 计算字符数的函数
)

split_documents = splitter.split_documents(documents)
print(len(split_documents))

for doc in split_documents:
    print("="*20,doc,"="*20)

