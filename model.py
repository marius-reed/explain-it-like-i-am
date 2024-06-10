from personas import personas
from openai import OpenAI
import os
import httpx

def chat_with_me_open_ai(model_name:str, system_message:str, user_input: str, _max_tokens:int=256) -> str:

    http_client = httpx.Client(verify=False)
    
    DATABRICKS_TOKEN = os.getenv('DB_WORKSPACE_TOKEN')
    client = OpenAI(
        api_key=DATABRICKS_TOKEN,
        base_url= os.getenv('DB_WORSKAPCE_SERVICE_ENDPOINT_URL'),
        http_client=http_client
    )

    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            "content": f"{system_message}"
        },
        {
            "role": "user",
            "content": f"{user_input}. Limit to {_max_tokens} tokens"
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



