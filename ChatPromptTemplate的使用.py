from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages([
    ('system', '你是一个边塞诗人'),
    MessagesPlaceholder(variable_name='history'),
    ('human', '再来一首唐诗'),
])

history_data = [
    ('human','你来一首唐诗'),
    ('ai','床前明月光，疑是地上霜。举头望明月，低头思故乡。'),
    ('human','好诗，再来一首'),
    ('ai','锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。')
]

prompt_text = chat_prompt_template.invoke(input={'history': history_data}).to_string()
print(prompt_text)

model = ChatTongyi(model='qwen3-max')
# response = model.invoke(prompt_text)
# print(response.content)

#通过chain调用
chain = chat_prompt_template | model
# response = chain.invoke(input={'history': history_data})
# print(response.content)
for chunk in chain.stream(input={'history': history_data}):
    print(chunk.content, end='', flush=True)
