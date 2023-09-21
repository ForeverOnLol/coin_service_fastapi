from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from coin_app.config import postgres_user, postgres_password, postgres_host, postgres_db

DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
ENGINE = create_engine(
    DATABASE_URL,
)
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

BASE = declarative_base()

# Dependency
def get_session():
    db = SESSION_LOCAL()
    try:
        return db
    finally:
        db.close()

