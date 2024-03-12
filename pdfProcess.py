import PyPDF2
import concurrent.futures
from langchain_community.document_loaders import PyPDFLoader
import time

pdfFileName = []
threadSafeList = []
max_threads = 100

def _split_pdf(input_pdf, output_folder):
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_number in range(len(pdf_reader.pages)):
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_number])
            pdfFileName.append(f"{output_folder}/page{page_number + 1}.pdf")
            output_file_path = f"{output_folder}/page{page_number + 1}.pdf"

            with open(output_file_path, 'wb') as output_file:
                pdf_writer.write(output_file)

def _process_chunk(file_name):
    loader = PyPDFLoader(f"{file_name}", extract_images=True)
    document = loader.load_and_split()
    threadSafeList.append(document[0])

def GetDataFromPDf(filename):
    _split_pdf(f"files/{filename}.pdf" , "split_pages")

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(_process_chunk, chunk) for chunk in pdfFileName]
        concurrent.futures.wait(futures)

    print(len(list(threadSafeList)))


def my_function():
    # Your function code here
    start_time = time.time()
    GetDataFromPDf('test')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    start_time = time.time()

    loader = PyPDFLoader(f"files/test.pdf", extract_images=True)
    document = loader.load_and_split()
    print(len(document))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
my_function()