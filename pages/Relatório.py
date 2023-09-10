import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/former_questions.csv", sep=";")

incorr = 0
corr = 0

for i in data.index:
  if data["graded"][i] and data["role"][i] == "assistant":
    if data["correct"][i]:
      corr = corr + 1
    else:
      incorr = incorr + 1

labels = 'Corretas', 'Incorretas'
sizes = [corr, incorr]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels)

st.pyplot(fig)