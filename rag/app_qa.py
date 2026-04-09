import streamlit as st
import config_data as config

from rag import RagService

st.title("智能客服")
st.divider()


prompt = st.chat_input()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，我是智能客服，我可以帮助你解决问题。"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    with st.spinner("thinking..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config = config.session_config)
        res_content = st.chat_message("assistant").write_stream(res_stream)
        st.session_state["message"].append({"role": "assistant", "content": res_content})
