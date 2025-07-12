import os
import logging
import sqlalchemy
from sqlalchemy import create_engine

LOG_DIR = "./log"
OUTPUT_DIR = "./output"

# Ensure log and output directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load database connection parameters from environment variables or use defaults
DB_USER = os.getenv("DB_USER",       "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST",       "localhost")
DB_PORT = os.getenv("DB_PORT",       "5432")
DB_NAME = os.getenv("DB_NAME",       "pafindb")

# Construct the SQLAlchemy database URL
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def get_logger(log_filename: str = None) -> logging.Logger:
    """
    Create and return a logger instance.
    If log_filename is provided, logs will be written to the specified file under LOG_DIR.
    """
    logger = logging.getLogger("bitflyer-crawler")
    if not logger.handlers:
        logging.basicConfig(
            filename=f"{LOG_DIR}/{log_filename}" if log_filename else None,
            filemode="a",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    return logger


def get_db() -> sqlalchemy.engine.Engine:
    """
    Create and return a SQLAlchemy engine for database operations.
    echo=True enables SQL statement logging for debugging.
    future=True enables SQLAlchemy 2.0 style usage.
    """
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    return engine
