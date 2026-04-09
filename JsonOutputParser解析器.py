from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(
    model='qwen3-max'
)

#第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "w我邻居姓{lastname}，刚生个{gender}，请起名字，仅告知我名字无需其他内容。"
    "请将json字符串返回，不要包含任何其他内容，key为name，value为你取的名字，请严格按照格式要求返回。"
)

#第二次提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解释含义。"
)

#构建链
chain = first_prompt | model | json_parser | second_prompt | model | str_parser
# res = chain.invoke({"lastname": "钦", "gender": "女儿"})
# print(res)

res = chain.stream({"lastname": "钦", "gender": "女儿"})
for chunk in res:
    print(chunk, end='', flush=True)

