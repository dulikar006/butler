import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from clients.mongo_client import MongoClient, MongoDBClient


def create_chroma(file_name):
    loader = PyPDFLoader(file_name)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )

    split_docs = text_splitter.split_documents(pages)
    uuid_list = [str(uuid.uuid4()) for _ in range(len(split_docs))]

    mc = MongoDBClient()
    mc.connect()

    mc.add_documents(split_docs, uuid_list)

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