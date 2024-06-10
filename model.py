from personas import personas
from openai import OpenAI
import os
import httpx
from databricks.vector_search.client import VectorSearchClient


def context_string_generator(user_input):

    workspace_url = os.getenv('DB_WORKSPACE_URL')
    sp_client_id = os.getenv('SP_CLIENT_ID')
    sp_client_secret = os.getenv('SP_CLIENT_SECRET')

    vsc = VectorSearchClient(
        workspace_url=workspace_url,
        service_principal_client_id=sp_client_id,
        service_principal_client_secret=sp_client_secret
    )

    index = vsc.get_index(endpoint_name="vs_endpoint", index_name="workspace.meetings.meeting_notes_index")
    # get context from vector search
    raw_context = index.similarity_search(columns=["text", "title"],
                            query_text=user_input,
                            num_results = 3)

    context_string = "Context:\n\n"

    for (i,doc) in enumerate(raw_context.get('result').get('data_array')):
        context_string += f"Retrieved context {i+1}:\n"
        context_string += doc[0]
        context_string += "\n\n"

    return context_string

def chat_with_me_open_ai(model_name:str, system_message:str, user_input: str, _max_tokens:int=256) -> str:

    http_client = httpx.Client(verify=False)
    
    DATABRICKS_TOKEN = os.getenv('DB_WORKSPACE_TOKEN')
    client = OpenAI(
        api_key=DATABRICKS_TOKEN,
        base_url= os.getenv('DB_WORSKAPCE_SERVICE_ENDPOINT_URL'),
        http_client=http_client
    )
    context_message = context_string_generator(user_input)
    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": f"{system_message}"
        },
        {
            "role": "user",
            "content": f"{context_message}. Limit to {_max_tokens} tokens"
        }
        ],
        model=model_name,
        max_tokens=_max_tokens
    )

    return chat_completion.choices[0].message.content



def query_model(persona: str, question: str, model_name = "databricks-meta-llama-3-70b-instruct") -> str:
    user_input = (question) # Based on user input in chat
    system_message = personas[persona] # Based on persona selection
    model_name = model_name # Based on model selection



    reply = chat_with_me_open_ai(model_name=model_name,system_message=system_message, user_input=user_input)
    return reply



