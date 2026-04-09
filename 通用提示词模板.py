from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("我的邻居姓{last_name}，刚生了{gender}，你帮我起个名字，简单回答。")

prompt_text = prompt_template.format_prompt(last_name='王', gender='男').to_string()
print(prompt_text)

model = Tongyi(
    model='qwen-max'
)
# res = model.invoke(input = prompt_text)
# print(res)

chain = prompt_template | model
res = chain.invoke(input={'last_name':'钦', 'gender':'男'})
print(res)