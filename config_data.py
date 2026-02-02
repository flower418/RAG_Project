# 固定存放 md5 文件的路径
md5_path = "./md5.txt"

# Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", "。", "！", "？", " ", ""]
max_split_char_number = 1000 # 文本分割的最大字符数