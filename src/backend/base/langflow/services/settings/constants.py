from typing_extensions import TypedDict

DEFAULT_SUPERUSER = "langflow"
DEFAULT_SUPERUSER_PASSWORD = "langflow"


class VariableDict(TypedDict):
    name: str
    default_fields: list[str]


VARIABLES_TO_GET_FROM_ENVIRONMENT: list[VariableDict] = [
    {"name": "OPENAI_API_KEY", "default_fields": ["openai_api_key"]},
    {"name": "ANTHROPIC_API_KEY", "default_fields": ["anthropic_api_key"]},
    {"name": "GOOGLE_API_KEY", "default_fields": ["google_api_key"]},
    {"name": "AZURE_OPENAI_API_KEY", "default_fields": ["azure_api_key"]},
    {"name": "AZURE_OPENAI_API_VERSION", "default_fields": ["azure_api_version"]},
    {"name": "AZURE_OPENAI_API_INSTANCE_NAME", "default_fields": ["azure_api_instance_name"]},
    {"name": "AZURE_OPENAI_API_DEPLOYMENT_NAME", "default_fields": ["azure_api_deployment_name"]},
    {"name": "AZURE_OPENAI_API_EMBEDDINGS_DEPLOYMENT_NAME", "default_fields": ["azure_api_embeddings_deployment_name"]},
    {"name": "ASTRA_DB_APPLICATION_TOKEN", "default_fields": ["astra_db_application_token"]},
    {"name": "ASTRA_DB_API_ENDPOINT", "default_fields": ["astra_db_api_endpoint"]},
    {"name": "COHERE_API_KEY", "default_fields": ["cohere_api_key"]},
    {"name": "GROQ_API_KEY", "default_fields": ["groq_api_key"]},
    {"name": "HUGGINGFACEHUB_API_TOKEN", "default_fields": ["huggingface_api_token"]},
    {"name": "PINECONE_API_KEY", "default_fields": ["pinecone_api_key"]},
    {"name": "SEARCHAPI_API_KEY", "default_fields": ["searchapi_api_key"]},
    {"name": "SERPAPI_API_KEY", "default_fields": ["serpapi_api_key"]},
    {"name": "UPSTASH_VECTOR_REST_URL", "default_fields": ["upstash_vector_rest_url"]},
    {"name": "UPSTASH_VECTOR_REST_TOKEN", "default_fields": ["upstash_vector_rest_token"]},
    {"name": "VECTARA_CUSTOMER_ID", "default_fields": ["vectara_customer_id"]},
    {"name": "VECTARA_CORPUS_ID", "default_fields": ["vectara_corpus_id"]},
    {"name": "VECTARA_API_KEY", "default_fields": ["vectara_api_key"]},
]
