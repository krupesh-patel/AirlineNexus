import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from tidb_vector.integrations import TiDBVectorClient

load_dotenv()


class TiDBConfig:
    def __init__(self):
        self.host = os.getenv('TIDB_HOST')
        self.port = int(os.getenv('TIDB_PORT', 4000))
        self.user = os.getenv('TIDB_USER')
        self.password = os.getenv('TIDB_PASSWORD')
        self.database = os.getenv('TIDB_DATABASE', 'airline_nexus')

    def get_connection_string(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?ssl_verify_cert=true&ssl_verify_identity=true"


class DatabaseManager:
    def __init__(self):
        self.config = TiDBConfig()
        self.engine = create_engine(
            self.config.get_connection_string(),
            pool_pre_ping=True,
            pool_recycle=300
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Initialize TiDB Vector Client for policy embeddings
        self.vector_client = None

    def get_session(self):
        return self.SessionLocal()

    def execute_query(self, query, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return result.fetchall()

    def get_vector_client(self, table_name='airline_policies', vector_dimension=384, recreate=False):
        """Get or create TiDB Vector Client"""
        if self.vector_client is None or recreate:
            self.vector_client = TiDBVectorClient(
                table_name=table_name,
                connection_string=self.config.get_connection_string(),
                vector_dimension=vector_dimension,
                drop_existing_table=recreate  # Drop existing table if recreate is True
            )
        return self.vector_client

    def check_data_exists(self):
        """Check if the necessary data already exists in the database"""
        try:
            import pymysql

            connection = pymysql.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                ssl=True,
                ssl_verify_cert=True,
                ssl_verify_identity=True
            )

            try:
                with connection.cursor() as cursor:
                    # Check if flights table exists and has data
                    cursor.execute("SELECT COUNT(*) FROM flights WHERE airline = 'AirlineNexus'")
                    flight_count = cursor.fetchone()[0]

                    # Check if vector table exists and has data
                    cursor.execute("SELECT COUNT(*) FROM airline_policies")
                    policy_count = cursor.fetchone()[0]

                    return flight_count > 0 and policy_count > 0

            finally:
                connection.close()

        except Exception as e:
            print(f"Error checking data existence: {e}")
            return False

    def create_tables(self):
        """Create necessary tables for the airline system (excluding vector table)"""
        import pymysql

        queries = [
            """
            CREATE TABLE IF NOT EXISTS flights (
                id INT PRIMARY KEY AUTO_INCREMENT,
                flight_number VARCHAR(10) NOT NULL,
                airline VARCHAR(50) NOT NULL,
                departure_airport VARCHAR(10) NOT NULL,
                arrival_airport VARCHAR(10) NOT NULL,
                departure_time DATETIME NOT NULL,
                arrival_time DATETIME NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                available_seats INT NOT NULL,
                aircraft_type VARCHAR(50),
                status VARCHAR(20) DEFAULT 'SCHEDULED'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS bookings (
                id INT PRIMARY KEY AUTO_INCREMENT,
                booking_reference VARCHAR(10) UNIQUE NOT NULL,
                flight_id INT NOT NULL,
                passenger_name VARCHAR(100) NOT NULL,
                passenger_email VARCHAR(100) NOT NULL,
                seat_number VARCHAR(10),
                booking_status VARCHAR(20) DEFAULT 'CONFIRMED',
                booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (flight_id) REFERENCES flights(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS support_tickets (
                id INT PRIMARY KEY AUTO_INCREMENT,
                ticket_id VARCHAR(20) UNIQUE NOT NULL,
                customer_email VARCHAR(100) NOT NULL,
                subject VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                status VARCHAR(20) DEFAULT 'OPEN',
                priority VARCHAR(10) DEFAULT 'MEDIUM',
                assigned_agent VARCHAR(100),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
        ]

        # Use pymysql directly to avoid SQLAlchemy parameter escaping issues
        connection = pymysql.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            ssl=True,
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

        try:
            with connection.cursor() as cursor:
                for query in queries:
                    try:
                        cursor.execute(query)
                        print(f"Table created successfully")
                    except Exception as e:
                        print(f"Error creating table: {e}")

            connection.commit()

        finally:
            connection.close()


db_manager = DatabaseManager()
