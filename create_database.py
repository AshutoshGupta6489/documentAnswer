import threading
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer  # Assuming SentenceTransformers for embedding model
from chromadb import chromadb

embedder = OllamaEmbeddings(model="mistral")
persistent_client = chromadb.PersistentClient()
collection = persistent_client.get_or_create_collection("my_pdf_embeddings")

def process_chunk(chunk):
    content = chunk.page_content
    embedding = embedder.embed_query(content)
    unique_id = f"{chunk.metadata['source']}-{chunk.metadata['page']}-{hash(content)}"
    collection.add(documents=[content], ids=[unique_id], embeddings=[embedding])


loader = PyPDFLoader("test.pdf")
document = loader.load_and_split()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(document)

# chunks[90].dict()
max_threads = 4
active_threads = 0

def process_next_chunk():
    global active_threads
    if active_threads < max_threads and len(chunks) > 0:
        chunk = chunks.pop(0)
        active_threads += 1
        thread = threading.Thread(target=process_chunk, args=(chunk,))
        thread.start()
        thread.join()
        active_threads -= 1
        print(f"Thread finished processing chunk...")

while len(chunks) > 0:
    process_next_chunk()
