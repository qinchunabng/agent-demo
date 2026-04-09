"""
提示词：用户提问+向量检索结果
"""
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


model = ChatTongyi(
    model="qwen3-max",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的问答助手，你的任务是根据用户的问题和向量检索结果，回答用户的问题，参考资料：{references}。"),
    ("user", "用户提问：{question}")
   ])

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(
        model="text-embedding-v4",
    )
)

#添加文档
vector_store.add_texts(["减肥就是要控制饮食，减少卡路里摄入","在减脂期间吃东西很重要，清淡少食，控制卡路里的输入，并保持运动。","跑步是很好的运动。"])

results = vector_store.similarity_search("如何减肥？",k=2)

referencing = "["
for result in results:
    if not result.page_content.endswith((".","。","?","!","！","？")):
        referencing += result.page_content + "。"
    else:
        referencing += result.page_content

referencing += "]"

print(referencing)

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()
res = chain.invoke({"question":"如何减肥？","references":referencing})
print(res)
