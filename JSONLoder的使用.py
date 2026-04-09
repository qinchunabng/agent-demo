from langchain_community.document_loaders import JSONLoader
import jq

loader = JSONLoader(
    file_path="./data/stus.json",
    jq_schema=".[].name", # 提取每个对象的name字段
    text_content=False, # 不加载文本内容，只加载JSON数据
)

document = loader.load()
print(document)
