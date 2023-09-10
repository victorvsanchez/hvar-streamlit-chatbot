import streamlit as st
import pandas as pd

data = pd.read_csv("data/former_questions.csv", sep=";")

for i in data.index:
    with st.chat_message(data["role"][i]):
        st.write(data["message"][i])
        if not data["graded"][i] and data["role"][i]=="assistant":
            st.write("Essa resposta está correta?")
            st.button("Sim", key=str(i) + "_yes")
            st.button("Não", key=str(i) + "_no")
        else:
            if data["correct"][i] and data["role"][i]=="assistant":
                st.write("Essa resposta foi avaliada como correta")
            else:
                st.write("Essa resposta foi avaliada como errada")