import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_HOST = os.getenv('MYSQL_HOST', 'host.docker.internal')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '00001')
MYSQL_DB = os.getenv('MYSQL_DB', 'doc_indo_db')

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
