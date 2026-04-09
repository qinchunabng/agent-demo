from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path='./data/stu.csv',
    csv_args={
        'delimiter': ',', # 自定义分隔符
        'fieldnames': ['name', 'age', 'gender'], # 自定义字段名，如果没有表头，需要指定字段名
    },
    encoding='utf-8',
)

#批量加载
# documents = loader.load()
#
# for doc in documents:
#     print(type(doc), doc)

#懒加载
for doc in loader.lazy_load():
    print(doc)