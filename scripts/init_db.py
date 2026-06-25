import os
import sys
from dotenv import load_dotenv

# Load .env from project root / smartgrid folder
repo_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(repo_root, "smartgrid", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

print("DATABASE_URL =", os.getenv("DATABASE_URL"))

try:
    # Import project DB objects
    from smartgrid.db.base import Base
    from smartgrid.db.session import engine

    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified successfully.")
    sys.exit(0)
except Exception as e:
    print("Failed to create/verify database tables:", type(e).__name__, str(e))
    sys.exit(1)
