import os
from dotenv import load_dotenv

load_dotenv("variables.env")
config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT"),
    "dbname":os.getenv("DB_NAME")
    }


import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")