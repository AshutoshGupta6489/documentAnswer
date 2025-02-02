import gradio as gr
import ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from pathlib import Path
from create_vectorstore import CreateVector

def vectordb(fileName):
    def file_exists_in_current_dir(file_name):
        current_dir = Path.cwd()
        file_path = current_dir / file_name
        return file_path.exists()

    embeddings = OllamaEmbeddings(model="mistral")

    if not file_exists_in_current_dir(f"dbs/{fileName}"):
        create_vector_instance = CreateVector()
        create_vector_instance.CreateVectors(fileName=fileName, threadCount=100, modelName="mistral")
    
    vectorstore = Chroma(persist_directory=f"./dbs/{fileName}", embedding_function = embeddings)

    retriever = vectorstore.as_retriever()
    return retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def ollama_llm(question, context):
    formatted_prompt = f"prompt: if answer is not available or have very less confidenece on the answer then return answer not in provided text \n\n Question: {question}\n\nContext: {context}"
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']

def rag_chain(question,fileName=None):
    if not fileName:
        fileName = 'chroma'
    retrieved_docs = vectordb(fileName).invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

ui = gr.Interface(
    fn=rag_chain,
    inputs=["text","text"],
    outputs=["text"]
)
# result = rag_chain("Can Additional depreciation be claimed on second hand machinery?")
# print(result)
ui.launch()