from pymongo import MongoClient
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from pymongo.operations import SearchIndexModel


class MongoDBClient:

    def __init__(self):
        self.url = 'mongodb+srv://dulikaranasinghe:UBhygr26Rr1jONQS@butler-db.841st.mongodb.net/?retryWrites=true&w=majority&appName=butler-db'
        self.vector_store = None
        self.atlas_collection = None
        self.db_name = "langchain_db"
        self.collection_name = "test"
        self.vector_search_index = "vector_index"

    def connect(self):
        client = MongoClient(self.url)
        # Define collection and index name

        self.atlas_collection = client[self.db_name][self.collection_name]

        embeddings = AzureOpenAIEmbeddings(
            # dimensions: Optional[int] = None, # Can specify dimensions with new text-embedding-3 models
            azure_endpoint="https://butler-openai.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15",
            api_key='b0a38c56c1c9454ea8c8c0ea1a804060',
            openai_api_version='2023-05-15',
            azure_deployment='text-embedding-ada-002'
        )

        self.vector_store = MongoDBAtlasVectorSearch(
            embedding=embeddings,
            collection=self.atlas_collection,
            index_name=self.vector_search_index
        )

    def create_index(self):
        # Create your index model, then create the search index
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "path": "embedding",
                        "numDimensions": 1536,
                        "similarity": "cosine"
                    },
                    {
                        "type": "filter",
                        "path": "page"
                    }
                ]
            },
            name=self.vector_search_index,
            type="vectorSearch"
        )
        self.atlas_collection.create_search_index(model=search_index_model)

    def add_documents(self, documents, ids):
        self.vector_store.add_documents(documents=documents, ids=ids)

    def delete_documents(self, ids_list: [str]):
        self.vector_store.delete(ids=ids_list)

    def search(self, query):
        results = self.vector_store.similarity_search(query=query, k=5)
        return [{'content': doc.page_content, 'metadata': doc.metadata} for doc in results]

    def search_with_filter(self, query, filter: [dict]):
        results = self.vector_store.similarity_search(query=query, k=1, post_filter=[{"bar": "baz"}])
        return [{'content': doc.page_content, 'metadata': doc.metadata} for doc in results]

    def search_with_score(self, query):
        results = self.vector_store.similarity_search_with_score(query=query, k=1)
        output = []
        for doc, score in results:
            output.append({'content': doc.page_content, 'score': score, 'metadata': doc.metadata})
        return output

    def lang_retriever(self, query):
        retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
        )
        return retriever.invoke(query)
