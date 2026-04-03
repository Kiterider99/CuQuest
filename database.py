import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

# 1. Check for the single Render-style URL first
# 2. Fall back to building it manually for your local setup
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # This part handles your local dev environment
    user = os.getenv("POSTGRES_USER")
    pw = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")
    
    if not all([user, pw, db]):
        raise RuntimeError("Database credentials are missing!")
        
    database_url = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"

# Render uses 'postgres://', but SQLAlchemy requires 'postgresql://'
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# The engine stays the same, but we use the unified URL
engine = create_engine(
    database_url, 
    pool_pre_ping=True,
    connect_args={"options": "-csearch_path=third_iteration"}
)

sessionlocal = sessionmaker(bind=engine)