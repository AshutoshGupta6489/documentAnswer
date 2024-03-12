from chromadb import chromadb

def CreateVectorDatabase(fileName):
    persistent_client = chromadb.PersistentClient(path=f"./dbs/{fileName if fileName else 'chroma'}")
    collection = persistent_client.get_or_create_collection("my_pdf_embeddings")
    return collection