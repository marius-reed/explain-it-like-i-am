import os
from databricks.vector_search.client import VectorSearchClient


workspace_url = os.getenv('DB_WORKSPACE_URL')
sp_client_id = os.getenv('SP_CLIENT_ID')
sp_client_secret = os.getenv('SP_CLIENT_SECRET')

vsc = VectorSearchClient(
    workspace_url=workspace_url,
    service_principal_client_id=sp_client_id,
    service_principal_client_secret=sp_client_secret
)

index = vsc.get_index(endpoint_name="vs_endpoint", index_name="workspace.vs_demo.fm_api_examples_vs_index")


def context_string_generator(user_input):
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


print(context_string_generator("Hello!"))