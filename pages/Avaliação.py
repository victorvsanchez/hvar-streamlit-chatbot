import streamlit as st

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant": 
            st.write("Essa resposta está correta?")
            st.button("Sim")
            st.button("Não")