import streamlit as st

counter = 0
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            counter = counter + 1
            st.write("Essa resposta está correta?")
            st.button("Sim", key=str(counter) + "_yes")
            st.button("Não", key=str(counter) + "_no")