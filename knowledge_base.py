import os
import config_data as config
import hashlib
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

# 检查传入的 md5 是否已经被处理过
# 如果没有则返回 False，表示需要处理
# 在存储中，md5.txt 是一行一个 md5 字符串，所以如果有一行相同，就直接返回 True
def check_md5(md5_str: str) -> bool:
    # 文件不存在，未处理过，返回 False
    if not os.path.exists(config.md5_path):
        # 不存在需要先创建文件
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        with open(config.md5_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                # 去除行尾换行符
                line = line.strip()
                if (line == md5_str):
                    return True
    return False

# 将传入的 md5 字符串记录到文件内保存
def save_md5(md5_str: str) -> None:
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")

# 将传入的字符串转换为 md5 字符串
def get_string_md5(input_str: str, encoding="utf-8") -> str:
    # 将字符串转为 byte 数组
    byte_str = input_str.encode(encoding=encoding)
    # 创建 md5 对象
    md5_obj = hashlib.md5()
    # 更新 md5 对象
    md5_obj.update(byte_str)
    # 获取 md5 字符串
    md5_hex = md5_obj.hexdigest()

    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        # 确保文件夹存在
        os.makedirs(config.persist_directory, exist_ok=True)
        # 相关配置信息放入配置文件
        self.chroma = Chroma(
            collection_name=config.collection_name, # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory # 数据库存储路径
        ) # 向量存储的实例，chroma 向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, # 分割后文本块最大长度
            chunk_overlap=config.chunk_overlap, # 连续文本段间的字符重叠数量
            separators=config.separators, # 自然段落间分隔的符号
            length_function=len # 默认使用 Python 自带
        ) # 文本切割器对象

    # 将传入的字符串进行向量化，存入数据库中
    def upload_by_str(self, data: str, filename: str) -> str:
        # 先获取字符串的 md5 值
        md5_hex = get_string_md5(data)
        # 检查 md5 是否已经处理过
        if check_md5(md5_hex):
            return "[跳过]内容已经在知识库中"

        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "me"
        }

        # 内容加载到向量库中
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        # 记录处理过相应 md5 数据
        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"