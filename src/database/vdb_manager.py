from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Define paths and embeddings
PERSIST_DIR = ".chroma"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # HuggingFace model for embeddings


class UploadFilesVDB:

    def __init__(self):
        self.vectorstore = None

    def connect(self):
        self.vectorstore = Chroma(
            collection_name="rag-hotel",
            persist_directory=PERSIST_DIR,
            embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        )

    def create_chroma(self, file_name):

        '''Function to create a Chroma vector store from documents'''



        loader = PyPDFLoader(file_name)
        pages = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=100, chunk_overlap=20
        )

        split_docs = text_splitter.split_documents(pages)


        vectorstore = Chroma.from_documents(
            documents=split_docs,
            collection_name="rag-hotel",
            # embedding=AzureOpenAIEmbeddings(model="text-embedding-3-large",
            #                                 api_key='9cae1c98f81247a7a02c8e0b3c2bee76',
            #                                 openai_api_version='2024-02-15-preview',
            #                                 azure_endpoint="https://mcap-eus-mts-ark-openai.openai.azure.com/openai/deployments/GPT_4o/chat/completions?api-version=2024-02-15-preview"
            #                                 ),
            embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
            persist_directory="./.chroma",
        )


    def search_chroma(self, query, source=None, category=None, top_k=5):
        '''Load the existing vector store'''

        # name_list = ['doc1', 'doc2', 'doc3']
        source_list = [source]
        category_list = [category]

        # Create filter dictionaries for each list
        # name_filter = {"name": {"$in": name_list}}
        source_filter = {"source": {"$in": source_list}}
        category_filter = {"Category": {"$in": category_list}}

        # Combine filters using $and or $or operators
        combined_filter = {
            "$and": [
                # name_filter,
                source_filter
                # category_filter
            ]
        }

        # base_retriever = self.vectorstore.as_retriever(search_kwargs={'k': top_k})
        # # Create the retriever with the combined filter
        # if source_filter:
        base_retriever = self.vectorstore.as_retriever(search_kwargs={'k': top_k}) #, 'filter': source_filter

        # Perform the query
        search_results = base_retriever.invoke(query)

        return search_results


# ufvdb = UploadFilesVDB()
# ufvdb.create_chroma('avani.pdf')
# ufvdb.update_chroma('sjb_blueprint.pdf')
# ufvdb.update_chroma('NPP Presidential Election Manifesto - 2024.pdf')


# ufvdb = UploadFilesVDB()
# ufvdb.connect()
# result = ufvdb.search_chroma('How does the SJB plan to achieve sustainable development and inclusive progress while leveraging innovation for long-term prosperity?', source='sjb_blueprint.pdf')
# print(result)
