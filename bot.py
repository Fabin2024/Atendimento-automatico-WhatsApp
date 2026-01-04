from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.db.postgres import PostgresDb
from dotenv import load_dotenv
import os

load_dotenv()


CACHE_REDIS_URI = os.getenv("CACHE_REDIS_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_CONNECTION_URI = os.getenv("DATABASE_CONNECTION_URI")

db = PostgresDb(
    db_url=DATABASE_CONNECTION_URI,
    db_schema="evolution_api",
)

vector_store = ChromaDb(
    collection="Manuais_collection",
    path="chroma_data",
    embedder=OpenAIEmbedder(
        api_key=OPENAI_API_KEY,
        id="text-embedding-3-small",
    ),
    persistent_client=True,
)


knowledge = Knowledge(
    vector_db=vector_store,
    
)



agente = Agent(
    knowledge=knowledge,
    name="Agente com contexto",
    search_knowledge=True,
    db=db,
    model=OpenAIChat(
        id="gpt-4o",
        api_key=OPENAI_API_KEY,
    ),
    add_memories_to_context=True,
    enable_user_memories=True,
    instructions= "você é um assistente virtual aonde resolverá todas as duvidas do cliente de forma educada e carismatica"
)

