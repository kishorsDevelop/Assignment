import os

user = os.environ.get('db_user')
password = os.environ.get('db_password')
host = os.environ.get('db_host')
name = os.environ.get('db_name')
SECRET_KEY = os.environ.get('secret_key')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}/{name}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
