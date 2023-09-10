import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

#import streamlit_authenticator as stauth
#import yaml
#from yaml.loader import SafeLoader

#with open('../config.yaml') as file:
#    config = yaml.load(file, Loader=SafeLoader)
#authenticator = Authenticate(
#    config['credentials'],
#    config['cookie']['name'],
#    config['cookie']['key'],
#    config['cookie']['expiry_days']
#)

#name, authentication_status, username = authenticator.login('Login', 'main')
#if authentication_status:
#    authenticator.logout('Logout', 'main')
#    st.write(f'Welcome *{name}*')
#    st.title('Some content')
#elif authentication_status == False:
#    st.error('Username/password is incorrect')
#elif authentication_status == None:
#    st.warning('Please enter your username and password')


st.set_page_config(page_title="Chatbot PWC - Documentos de RH", layout="centered", initial_sidebar_state="auto", menu_items=None)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

openai.api_key = openai_api_key
st.title("Chatbot PWC - Documentos de RH 💬")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Me faça uma pergunta sobre a política de férias da PWC!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Carregando os documentos..."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="Responda à pergunta em português. Use apenas o documento carregado para responder à pergunta. Se você não sabe a resposta, diga 'desculpe, eu não sei a resposta para essa pergunta', não tente dar uma resposta. Use no máximo três frases e mantenha a resposta o mais concisa possível. Sempre diga 'obrigado por perguntar!' ao final da resposta."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()
# chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features.")
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history