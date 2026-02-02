# 基于 streamlit 完成 web 网页上传服务
import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新服务")

uploaded_file = st.file_uploader(
    "请上传 txt 文件",
    type=["txt"], # 仅允许上传 txt 文件
    accept_multiple_files=False # 仅允许单文件上传
)

# 创建 st.session_state，存储 KnowledgeBaseService 实例
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 如果成功上传了文件
if uploaded_file is not None:
    # 提取文件内容
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024  # 转换为 KB

    st.subheader(f"文件名: {file_name}")
    st.write(f"大小: {file_size:.2f}KB, 类型: {file_type}")

    # 获取文件内容
    text = uploaded_file.getvalue().decode("utf-8")
    st.write(text)

    with st.spinner("正在上传到知识库，请稍候..."):
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)