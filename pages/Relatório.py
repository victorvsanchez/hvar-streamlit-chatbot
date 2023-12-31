import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#Load history data
data = pd.read_csv("data/former_questions.csv", sep=";")
#Add new data
msg_num = 0
for message in st.session_state.messages:
    msg_num = msg_num + 1
    new_record = ["Admin", msg_num, message["role"], message["content"], 0, 1]
    data.loc[len(data.index)] = new_record

### Porcentagem de perguntas corretas
incorr = 0
corr = 0

for i in data.index:
  if data["graded"][i] and data["role"][i] == "assistant":
    if data["correct"][i]:
      corr = corr + 1
    else:
      incorr = incorr + 1

labels = 'Corretas', 'Incorretas'
answers = [corr, incorr]
fig1 = px.pie(values=[corr, incorr], names=["Respostas corretas", "Respostas incorretas"])

st.header("Precisão das respostas")
st.plotly_chart(fig1, theme=None, use_container_width=True)

### Número de perguntas
df_counts = data[data['role']=='user'].groupby('user').count().reset_index()[['user', 'message']]
df_counts.rename(columns={'user': 'Usuário', 'message': 'Número de mensagens'}, inplace=True)
fig2 = go.Figure(go.Bar(
            x=df_counts["Número de mensagens"],
            y=df_counts["Usuário"],
            orientation='h'))

st.header("Número de perguntas por usuário")
st.plotly_chart(fig2, theme=None, use_container_width=True)

### Número de requisições por dia
days = [i+1 for i in range(14)] + [i+1 for i in range(14)]
dataframe = pd.DataFrame(np.random.randint(low=0, high=10, size = (len(days), 1)).tolist(), columns=["Número de respostas"])
dataframe["Dia"] = days
status = ["Respostas corretas" for i in range(14)] + ["Respostas incorretas" for i in range(14)]
dataframe["Status"] = status
fig3 = px.line(dataframe, x="Dia", y="Número de respostas", color='Status')

st.header("Número de requisições por dia")
st.plotly_chart(fig3, theme=None, use_container_width=True)