from langchain_community.llms.tongyi import Tongyi

model = Tongyi(
    model='qwen-plus',
)

# res = model.invoke(input="你是谁啊？能做什么？")
# print(res)

#流式
res = model.stream(input="你是谁啊？能做什么？")

for chunk in res:
    print(chunk, end="", flush=True)
