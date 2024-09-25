from clients.openai_client import llm
from database.vdb_manager import UploadFilesVDB


def load_from_vector(type, query):
    if type == "SJB":
        source = 'sjb_blueprint.pdf'
    elif type == "NPP":
        source = 'NPP Presidential Election Manifesto - 2024.pdf'
    else:
        return

    ufvdb = UploadFilesVDB()
    ufvdb.connect()
    search_results = ufvdb.search_chroma(query, source=source)
    search_results_text = "\n".join([doc.page_content for doc in search_results])
    return search_results_text

def generate_response(query):
    type = "SJB"
    data = load_from_vector(type, query)

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
