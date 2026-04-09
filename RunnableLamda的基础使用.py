from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()

model = ChatTongyi(
    model='qwen3-max'
)

#第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "w我邻居姓{lastname}，刚生个{gender}，请起名字，仅告知我名字无需其他内容。"
)

#第二次提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解释含义。"
)

# my_func = RunnableLambda(lambda ai_msg: { 'name': ai_msg.content })

chain = first_prompt | model | (lambda ai_msg: { 'name': ai_msg.content }) | second_prompt | model | str_parser
for chunk in chain.stream({"lastname": "钦", "gender": "女儿"}):
    print(chunk, end='', flush=True)
