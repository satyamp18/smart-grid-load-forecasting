import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def main():
    # Load .env from smartgrid folder if present
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "smartgrid", ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not found in environment or smartgrid/.env")
        sys.exit(2)

    print("Using DATABASE_URL:", db_url)

    try:
        engine = create_engine(db_url, connect_args={})
        with engine.connect() as conn:
            row = conn.execute(text("SELECT version();")).fetchone()
            print("Connected to PostgreSQL:", row[0])
    except Exception as e:
        print("Failed to connect to PostgreSQL:", type(e).__name__, str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
