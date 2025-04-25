# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = f"oracle+oracledb://{os.getenv('DATABASE_DCAF_USER')}:{os.getenv('DATABASE_DCAF_PASSWORD')}@{os.getenv('DATABASE_DCAF_HOST')}:{os.getenv('DATABASE_DCAF_PORT')}/{os.getenv('DATABASE_DCAF_SID')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
