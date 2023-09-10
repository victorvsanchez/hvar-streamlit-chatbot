import streamlit as st
import pandas as pd

#Load history data
data = pd.read_csv("data/former_questions.csv", sep=";")
#Add new data
msg_num = 0
for message in st.session_state.messages:
    new_record = ["Admin", msg_num, message["role"], message["content"], 0, 1]
    if msg_num >= 1:
        data.loc[len(data.index)] = new_record
    msg_num = msg_num + 1

for i in data.index:
    with st.chat_message(data["role"][i]):
        st.write(data["message"][i])
        if not data["graded"][i] and data["role"][i]=="assistant":
            st.write("Essa resposta não foi avaliada ainda. Ela está correta?")
            if st.button("Sim", key=str(i) + "_hist_yes"):
                st.write("Yes")
            if st.button("Não", key=str(i) + "_hist_no"):
                st.write("No")

        else:
            if data["correct"][i] and data["role"][i]=="assistant":
                st.write("Essa resposta foi avaliada como correta")
            elif not data["correct"][i] and data["role"][i]=="assistant":
                st.write("Essa resposta foi avaliada como errada")
        if data["role"][i] == "assistant":
            st.divider()