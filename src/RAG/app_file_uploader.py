import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

st.title("知识库文件更新服务")


uploaded_file = st.file_uploader("选择文件",
                                  type=["txt", "pdf", "docx"]
                                  )


if "counter" not in st.session_state:
    st.session_state["counter"] =0
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploaded_file is not None:
    filename = uploaded_file.name
    st.write("文件名:", uploaded_file.name)
    st.write("文件类型:", uploaded_file.type)
    st.write("文件大小:", uploaded_file.size, "字节")

    st.subheader("文件内容预览")
    text = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("正在处理..."):
        time.sleep(3)
        res = st.session_state["service"].add_knowledge(text,filename)
        st.write(res)
        st.session_state["counter"] += 1

print(f"上传了：{st.session_state["counter"]}个文件")