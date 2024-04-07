import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = b'\x81\xc9Pi\xaa"\xd8L\xaf\xc6a,'
    DBMS = os.getenv("DBMS")
    DB_HOST = os.getenv(f"{DBMS}_HOST")
    DB_PORT = os.getenv(f"{DBMS}_PORT")
    DB_USER = os.getenv(f"{DBMS}_USER")
    DB_PASSWORD = os.getenv(f"{DBMS}_PASSWORD")
    DB_NAME = os.getenv(f"{DBMS}_DB")


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    DBMS = os.getenv("DBMS")
    DB_NAME = os.getenv(f"TEST_{DBMS}_DB")
    TESTING = True
