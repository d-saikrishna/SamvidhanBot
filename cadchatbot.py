from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceHubEmbeddings
from langchain_community import embeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEndpoint

import streamlit as st
import os
from os.path import join
import time 
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.callbacks import LangChainTracer
from langsmith import Client
langsmith_key = os.getenv("LANGSMITH_API_KEY")

callbacks = [
LangChainTracer(
  project_name="cad",
  client=Client(
    api_url="https://api.smith.langchain.com",
    api_key=langsmith_key
  )
)
]



from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

# Access the API key
hf_key = os.getenv("HF_TOKEN")
from PIL import Image
im = Image.open("assets/favicon-32x32.png")

st.set_page_config(
    page_title="CAD",
    page_icon=im)
# Following line will help in seeing dynamic session states
# "st.session_state object:" , st.session_state

# Vector Embedding and Vector Store

dir = os.getcwd()

db_disk = Chroma(
    #embedding_function=OllamaEmbeddings(model='llama3.2'),
    embedding_function=HuggingFaceHubEmbeddings(model='sentence-transformers/all-mpnet-base-v2',
                                                huggingfacehub_api_token=hf_key),
    persist_directory=dir+"/db",
)

#Design Prompt Template
prompt = ChatPromptTemplate.from_template("""Answer the following question strictly based on provided context.
                                          The context provided is the debates from the Constitutional Assembly of India.
                                          Give the answer in bullet points. Include quotes if necessary.
                                          Execute Python codes if needed to answer for any calculations, don't print code in the answer.
                                          <context>
                                          {context}
                                          <context>
                                          Question: {input}""")


st.title("Talk to the people who made Indian Constitution!")
#model = OllamaLLM(model="llama3.2")
models = ['MistralAI', 'Google Gemma']
llm_model = st.selectbox("Select a LLM Model: ", models, placeholder ="Choose LLM Model")

questions = ["Custom query"]
with open(join("questions.txt")) as f:
    questions += f.read().split("\n")

query = st.selectbox("Select a query: ", questions, index=None, placeholder ="Choose Custom query to ask your own question")

if llm_model=="MistralAI":
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
elif llm_model=="Google Gemma":
    repo_id = "google/gemma-2-2b-it"
else:
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"#"deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"

model = HuggingFaceEndpoint(repo_id = repo_id, max_length=1000, temperature=0.5,token=hf_key)

document_chain = create_stuff_documents_chain(model, prompt)
retriever = db_disk.as_retriever(search_type="mmr", 
                                 search_kwargs={"k": 20, "fetch_k": 50, "lambda_mult":1,
                                                })

retrieval_chain = create_retrieval_chain(retriever, document_chain)
answer=''

if query == "Custom query":
    query = st.text_input("Ask your question",)

with st.form(key='my_form_to_submit'):
    submit_button = st.form_submit_button(label='Submit')

    
if submit_button:
    with st.spinner('Wait for it...'):
        time.sleep(5)
        config={"callbacks": callbacks}
        response = retrieval_chain.invoke({"input":query}, config=config)
        answer = response['answer']
    st.write(answer)
