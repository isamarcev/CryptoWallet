import os

from databases import Database
from sqlalchemy import create_engine, MetaData

#
from sqlalchemy.orm import sessionmaker

from base_api.config.settings import settings


#print(settings.loc)
DATABASE_URL = str(settings.postgres_url)
# DATABASE_URL = 'postgresql://nikitin:admin@localhost/crypto_wallet_base'

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.create_all(engine)
# конструктор запитів бази даних
database = Database(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
