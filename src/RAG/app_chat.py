import streamlit as st
import time
from rag_service import RagService

st.title("知识库智能客服")
st.divider()

if "service" not in st.session_state:
    st.session_state["service"] = RagService()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant", "content":"你好，我是知识库智能客服，你可以向我提问任何问题。"}]

for message in st.session_state["message"]:
    st.chat_message("role").write(message["content"])

prompt = st.chat_input("请输入问题")

if prompt:
    st.chat_message("user").write(prompt)

    st.session_state["message"] .append({"role":"user", "content":prompt})
    ai_res_list = []
    with st.spinner("思考中..."):
        time.sleep(3)
        res_stream = st.session_state["service"].get_answer(prompt)

        # yield
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        st.session_state["message"] .append({"role":"assistant", "content":"".join(ai_res_list)})

