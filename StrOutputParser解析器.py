from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi

from langchain_core.prompts import PromptTemplate

model = ChatTongyi(
    model='qwen3-max'
)
prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname}，刚生了{gender}，请起名字，仅告知我名字无需其他内容"
)
parser = StrOutputParser()
chain = prompt | model | parser| model | parser
res = chain.invoke({"lastname": "王", "gender": "男"})
print(res)
print(type(res))
