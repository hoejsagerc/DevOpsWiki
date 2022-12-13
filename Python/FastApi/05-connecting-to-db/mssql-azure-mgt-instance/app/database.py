# Importing Standard Python Modules
import os
import requests
import pyodbc
import urllib
import struct
import logging
# Import sqlalchemy modules
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Retrieving Database Values from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
MSI_ENDPOINT = os.getenv('MSI_ENDPOINT')
MSI_SECRET = os.getenv('MSI_SECRET')
DRIVER = '{FreeTDS}'  # os.getenv('DRIVER')


def get_bearer_token(resource_uri, token_api_version):
    token_auth_uri = f"{MSI_ENDPOINT}?resource={resource_uri}&api-version={token_api_version}"
    head_msi = {'Secret':MSI_SECRET}
    resp = requests.get(token_auth_uri, headers=head_msi)
    print('New token for the database has been aquired by the managed identity')
    try:
        access_token = resp.json()['access_token']
        print('New token for the database has been aquired by the managed identity')
    except IndexError:
        print("MSI: No access token found in response")
        raise
    return access_token


connstr=f"Driver={DRIVER};Server={DB_HOST},1433;Database={DB_NAME}"

token = bytes(get_bearer_token("https://database.windows.net/", "2021-11-01'"), "UTF-8")
exptoken = b""
for i in token:
    exptoken += bytes({i})
    exptoken += bytes(1)

tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

params = urllib.parse.quote(connstr)
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params) ,connect_args={'attrs_before': { 1256:tokenstruct}})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()