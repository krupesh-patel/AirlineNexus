import json
import os

from dotenv import load_dotenv
from tidb_vector.integrations import TiDBVectorClient

from utils.embeddings import embedding_service

load_dotenv()


def ingest_airline_policies() -> str:
    """Ingest airline policies with vector embeddings using TiDBVectorClient"""
    try:
        with open('data/airline_policies.json', 'r') as f:
            policies = json.load(f)

        # Prepare data for TiDBVectorClient
        ids = []
        texts = []
        embeddings = []
        metadatas = []

        for i, policy in enumerate(policies):
            # Generate embedding for the policy content
            embedding = embedding_service.embed_text(policy['content'])

            ids.append(str(i + 1))
            texts.append(policy['content'])
            embeddings.append(embedding)
            metadatas.append({
                'category': policy['category'],
                'title': policy['title']
            })

        # Retrieve environment variables
        host = os.getenv('TIDB_HOST')
        port = int(os.getenv('TIDB_PORT', 4000))
        user = os.getenv('TIDB_USER')
        password = os.getenv('TIDB_PASSWORD')
        database = os.getenv('TIDB_DATABASE', 'airline_nexus')

        # Generate the connection string
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?ssl_verify_cert=true&ssl_verify_identity=true"

        vector_client = TiDBVectorClient(
            table_name="airline_policies",
            connection_string=connection_string,
            vector_dimension=384,
            drop_existing_table=True  # Drop existing table if recreate is True
        )

        # Use TiDBVectorClient to insert data
        vector_client.insert(
            ids=ids,
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return f"Successfully ingested {len(policies)} airline policies with embeddings using TiDBVectorClient"

    except Exception as e:
        raise Exception(f"Failed to ingest airline policies: {str(e)}")


ingest_airline_policies()
