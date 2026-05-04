import streamlit as st
from agent.react_agent import ReactAgent

st.title("智扫通智能机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state.agent = ReactAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

#用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("智能客服思考中..."):
        res = st.session_state.agent.execute_stream(prompt)
        content = st.chat_message("assistant").write_stream(res)
        st.session_state.messages.append({"role": "assistant", "content": content})

