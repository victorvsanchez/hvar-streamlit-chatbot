import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/former_questions.csv", sep=";")

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
fig, ax = plt.subplots()
ax.pie(answers, labels=labels)

st.write("Precisão das respostas")
st.pyplot(fig)

### Número de perguntas
df_counts = data[data['role']=='user'].groupby('user').count().reset_index()[['user', 'message']]
df_counts.rename(columns={'user': 'Usuário', 'message': 'Número de mensagens'}, inplace=True)
chart_data = df_counts

st.write("Número de perguntas por usuário")
st.bar_chart(chart_data)

### Número de requisições por dia
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns = ['Número de perguntas', 'Respostas incorretas', 'Respostas corretas'])

st.write("Número de requisições por dia")
st.line_chart(
    chart_data,
    x = 'Número de perguntas',
    y = ['Respostas incorretas', 'Respostas corretas'],
    color = ['#FF0000', '#008000'] 
)