# Importing Standard Python Modules
import os
import pyodbc
import urllib
import logging
# Import sqlalchemy modules
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Retrieving Database Values from environment variables
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
MSI_ENDPOINT = os.getenv('MSI_ENDPOINT')
MSI_SECRET = os.getenv('MSI_SECRET')
DRIVER = '{FreeTDS}'  # os.getenv('DRIVER')


engine = create_engine(
            'mssql+pyodbc:///?odbc_connect=%s' % (
                urllib.parse.quote_plus(
                    'DRIVER={FreeTDS};' + f'SERVER={DB_HOST};'
                    f'DATABASE={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD};port=1433;'
                    'TDS_Version=8.0;'
                )
            )
        )


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()