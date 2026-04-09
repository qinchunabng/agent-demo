md5_path = "./md5.txt"
collection_name = "rag"
embedding_function = ""
persist_directory = "./chroma_db"

chunk_size = 50
chunk_overlap = 0
separators = ["\n", "。", "!", "！", "?", "？", ".", " ", ""]
max_split_char_number = 30

#检索返回的匹配的文档数
similarity_threshold = 1

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"