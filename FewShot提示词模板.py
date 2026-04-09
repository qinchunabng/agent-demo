from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate


# 示例的模板
example_template = PromptTemplate.from_template("单词：{word}，反义词：{antonym}")

# 示例的动态数据注入，要求是list内嵌套字典
examples_data = [
    {'word': '好', 'antonym': '坏'},
    {'word': '大', 'antonym': '小'},
    {'word': '上', 'antonym': '下'},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_template,    #示例数据模板
    examples=examples_data,          #示例数据（用来注入动态数据的），list内嵌套字典
    prefix='告知我单词的反义词，我提供如下的示例：',            #示例之前的提示词
    suffix='请根据示例，填写单词{word}的反义词。',            #示例之后的提示词
    input_variables=['word'],     #输入变量，用来注入动态数据的
)

prompt_text = few_shot_template.invoke(input={'word':'左'}).to_string()
print(prompt_text)

model = Tongyi(model='qwen-max')
response = model.invoke(input=prompt_text)
print(response)