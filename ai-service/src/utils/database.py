import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured in the environment."
    )


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """
    return psycopg.connect(DATABASE_URL)