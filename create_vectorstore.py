import threading
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from create_database_filename import CreateVectorDatabase

class CreateVector():
    def __init__(self) -> None:
        self.active_threads = 0  # Variable to keep track of active threads

    def CreateVectors(self, fileName, threadCount=100, modelName='mistral'):
        """
        Method to create vectors from a PDF document using multi-threading.

        Parameters:
        - fileName (str): The name of the PDF file to process.
        - threadCount (int): The maximum number of threads to use.
        - modelName (str): The name of the embedding model to use. Default is 'mistral'.
        """
        # Initialize embedding model and database collection
        embedder = OllamaEmbeddings(model=modelName)
        collection = CreateVectorDatabase(fileName)

        def process_chunk(chunk):
            """
            Process a chunk of text from a PDF document.

            Parameters:
            - chunk: A chunk of text from the document.
            """
            content = chunk.page_content
            embedding = embedder.embed_query(content)
            unique_id = f"{chunk.metadata['source']}-{chunk.metadata['page']}-{hash(content)}"
            collection.add(documents=[content], ids=[unique_id], embeddings=[embedding])

        # Load and split the PDF document
        loader = PyPDFLoader(f"files/{fileName}.pdf", extract_images=True)
        document = loader.load_and_split()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(document)

        max_threads = threadCount

        def process_next_chunk():
            """
            Process the next available chunk using multi-threading.
            """
            nonlocal chunks
            if self.active_threads < max_threads and len(chunks) > 0:
                chunk = chunks.pop(0)
                self.active_threads += 1
                thread = threading.Thread(target=process_chunk, args=(chunk,))
                thread.start()
                thread.join()
                self.active_threads -= 1
                print(f"Thread finished processing chunk...")

        # Process chunks using multi-threading
        while len(chunks) > 0:
            process_next_chunk()
        return collection
