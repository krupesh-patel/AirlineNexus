import json
import os
from typing import Dict, Any, List

from tidb_vector.integrations import TiDBVectorClient

from config.database import db_manager
from utils.embeddings import embedding_service
from dotenv import load_dotenv

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


def ingest_sample_flights() -> str:
    """Ingest sample flight data"""
    try:
        import pymysql

        with open('data/sample_flights.json', 'r') as f:
            flights = json.load(f)

        # Use pymysql directly to avoid SQLAlchemy parameter escaping issues
        config = db_manager.config
        connection = pymysql.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
            ssl=True,
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

        try:
            with connection.cursor() as cursor:
                # Clear existing flight data first to avoid duplicates
                cursor.execute("DELETE FROM flights WHERE airline = 'AirlineNexus'")

                for flight in flights:
                    query = """
                    INSERT INTO flights (flight_number, airline, departure_airport, arrival_airport,
                                       departure_time, arrival_time, price, available_seats, 
                                       aircraft_type, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (
                        flight['flight_number'],
                        flight['airline'],
                        flight['departure_airport'],
                        flight['arrival_airport'],
                        flight['departure_time'],
                        flight['arrival_time'],
                        flight['price'],
                        flight['available_seats'],
                        flight['aircraft_type'],
                        flight['status']
                    )

                    cursor.execute(query, values)

            connection.commit()

        finally:
            connection.close()

        return f"Successfully ingested {len(flights)} sample flights"

    except Exception as e:
        raise Exception(f"Failed to ingest sample flights: {str(e)}")


ingest_airline_policies()
ingest_sample_flights()