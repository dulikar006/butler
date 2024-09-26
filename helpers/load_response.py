from clients.mongo_client import MongoDBClient
from clients.openai_client import llm


def load_from_vector(query):

    mc = MongoDBClient()
    mc.connect()
    search_results = mc.search(query)
    search_results_text = "\n".join([doc.get('content') for doc in search_results])
    return search_results_text

def generate_response(query):
    data = load_from_vector(query)

    prompt = f"""You are a personal assistant at Avani Hotel dedicated to the customer in Room number 103.
    Your job is to refer the knowledge content and guide your customer as best and humble way possible.
    Please do not misguide or use any extra information out of the knowledge content.
    Below content is the knowledge related to the information your customer might need.
    [content starts here]
    {data}
    [content ends here]
    
    Please answer this question only based on the knowledge.
    Question: {query}
    
    return maximum of 50 words consolidated, summarize answer in most simple and humble way possible
    """
    return llm(prompt)
