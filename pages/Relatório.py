import streamlit as st
import pandas as pd
import plotly.express as px
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
fig = px.pie(df, values=[corr, incorr], names=["Respostas corretas", "Respostas incorretas"])

st.header("Precisão das respostas")
st.plotly_chart(fig, theme=None, use_container_width=True)

### Número de perguntas
df_counts = data[data['role']=='user'].groupby('user').count().reset_index()[['user', 'message']]
df_counts.rename(columns={'user': 'Usuário', 'message': 'Número de mensagens'}, inplace=True)
chart_data = df_counts

st.header("Número de perguntas por usuário")
st.bar_chart(chart_data)

### Número de requisições por dia
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns = ['Número de perguntas', 'Respostas incorretas', 'Respostas corretas'])

st.header("Número de requisições por dia")
st.line_chart(
    chart_data,
    x = 'Número de perguntas',
    y = ['Respostas incorretas', 'Respostas corretas'],
    color = ['#FF0000', '#008000'] 
)