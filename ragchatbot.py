from langchain_community.embeddings import OllamaEmbeddings
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

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

# Access the API key
hf_key = os.getenv("HF_TOKEN")
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"

st.set_page_config(layout="wide", page_title="Samvidhan")
# Following line will help in seeing dynamic session states
# "st.session_state object:" , st.session_state

# Vector Embedding and Vector Store

dir = os.getcwd()

db_disk = Chroma(
    embedding_function=OllamaEmbeddings(model='llama3.2'),
    persist_directory=dir+"/db",
)

#Design Prompt Template
prompt = ChatPromptTemplate.from_template("""Answer the following question strictly based on provided context. 
                                          Execute Python codes if needed to answer for any calculations, don't print code in the answer.
                                          <context>
                                          {context}
                                          <context>
                                          Question: {input}""")


#model = OllamaLLM(model="llama3.2")
model = HuggingFaceEndpoint(repo_id = repo_id, max_length=128, temperature=0.7,token=hf_key)

document_chain = create_stuff_documents_chain(model, prompt)
retriever = db_disk.as_retriever(search_type="mmr", 
                                 search_kwargs={"k": 20, "fetch_k": 50, "lambda_mult":1,
                                                })

retrieval_chain = create_retrieval_chain(retriever, document_chain)

questions = ["Custom query"]
with open(join("questions.txt")) as f:
    questions += f.read().split("\n")

st.title("Talk to the people who made constitution!")
answer=''

query = st.selectbox("Select a query: ", questions, index=None, placeholder ="Choose Custom query to ask your own question")

if query == "Custom query":
    query = st.text_input("Ask your question",)

with st.form(key='my_form_to_submit'):
    submit_button = st.form_submit_button(label='Submit')

    
if submit_button:
    response = retrieval_chain.invoke({"input":query})
    answer = response['answer']
    st.write(answer)