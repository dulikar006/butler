import base64
import os
from io import BytesIO

from langchain_core.documents import Document
from pypdf import PdfReader

from clients.mongo_client import MongoDBClient

import uuid
import pandas as pd
from PIL import Image

from langchain.text_splitter import RecursiveCharacterTextSplitter

from clients.openai_client import llm


def upload_file(file_name, file_content):
    try:
        _, file_type = os.path.splitext(file_name)
        file_type = file_type.lower().replace('.', '')  # Normalize the file type

        mc = MongoDBClient()
        mc.connect()

        split_docs = []

        if file_type == 'pdf':
            # Handle PDF from bytes
            with BytesIO(file_content) as pdf_stream:
                # loader = PyPDFLoader(pdf_stream)
                # pages = loader.load_and_split()
                reader = PdfReader(pdf_stream)  # Use PdfReader directly
                pages = [page.extract_text() for page in reader.pages if page.extract_text()]  # Extract text from pages

                documents = [Document(page_content=page) for page in pages if page]

                # Split documents into chunks
                text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                    chunk_size=100, chunk_overlap=20
                )
                split_docs = text_splitter.split_documents(documents)

        elif file_type == 'csv':
            # Handle CSV from bytes
            df = pd.read_csv(BytesIO(file_content))
            pages = df.to_dict(orient='records')  # Convert DataFrame to list of dicts
            split_docs = [Document(page_content=str(page)) for page in pages if page]


        elif file_type in ['xls', 'xlsx']:
            # Handle Excel from bytes
            df = pd.read_excel(BytesIO(file_content))
            pages = df.to_dict(orient='records')
            split_docs = [Document(page_content=str(page)) for page in pages if page]

        elif file_type in ['jpg', 'jpeg', 'png']:
            # Create a BytesIO object to save the image
            buffered = BytesIO()
            image = Image.open(BytesIO(file_content))
            image.save(buffered, format="JPEG")  # You can change the format as needed
            # Get the base64-encoded string
            base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
            pages = llm(base64_string)
            split_docs = [Document(page_content=page) for page in pages if page]

        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Generate UUIDs for the documents
        uuid_list = [str(uuid.uuid4()) for _ in range(len(split_docs))]

        # Add documents to MongoDB
        mc.add_documents(split_docs, uuid_list)

        return uuid_list  # Return the list of generated UUIDs
    except Exception as err:
        print(f"Error while uploading documents to MongoDB - {err}")
        return False



def upload_information(information):
    mc = MongoDBClient()
    mc.connect()

    custom_documents = []
    custom_doc = Document(
        page_content=information,  # The text content of the document chunk
        metadata={}
    )
    custom_documents.append(custom_doc)

    # Generate UUIDs for the documents
    uuid_list = [str(uuid.uuid4()) for _ in range(len(custom_documents))]

    # Add documents to MongoDB
    mc.add_documents(custom_documents, uuid_list)

def search_chroma(query):

    mc = MongoDBClient()
    mc.connect()
    search_results = mc.search(query)

    return search_results


# create_chroma('avani.pdf')


# mc = MongoDBClient()
# mc.connect()
# mc.create_index()


#
# result = search_chroma("yoga")
#
# for i in result:
#     print(i)