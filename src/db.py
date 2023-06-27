import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV_DB', 'user')
password = config.get('DEV_DB', 'password')
db_name = config.get('DEV_DB', 'db_name')
domain = config.get('DEV_DB', 'domain')

url = f'postgresql://{username}:{password}@{domain}:5432/{db_name}'

engine = create_engine(url, echo=False, pool_size=5, max_overflow=0)

DBSession = sessionmaker(bind=engine)
session = DBSession()
session = DBSession()