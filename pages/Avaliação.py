import streamlit as st
import pandas as pd

#Load history data
data = pd.read_csv("data/former_questions.csv", sep=";")
#Add new data
msg_num = 0
for message in st.session_state.messages:
    msg_num = msg_num + 1
    new_record = ["Admin", msg_num, message["role"], message["content"], 0, 1]
    data.loc[len(data.index)] = new_record

for i in data.index:
    with st.chat_message(data["role"][i]):
        st.write(data["message"][i])
        if not data["graded"][i] and data["role"][i]=="assistant":
            st.write("Essa resposta não foi avaliada ainda. Ela está correta?")
            st.button("Sim", key=str(i) + "_hist_yes")
            st.button("Não", key=str(i) + "_hist_no")
        else:
            if data["correct"][i] and data["role"][i]=="assistant":
                st.write("Essa resposta foi avaliada como correta")
            elif not data["correct"][i] and data["role"][i]=="assistant":
                st.write("Essa resposta foi avaliada como errada")
        if data["role"][i] == "assistant":
            st.divider()