import os

from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

#
from base_api.config.settings import settings


#print(settings.loc)
DATABASE_URL = str(settings.postgres_url)

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.create_all(engine)

# конструктор запитів бази даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(DATABASE_URL)
