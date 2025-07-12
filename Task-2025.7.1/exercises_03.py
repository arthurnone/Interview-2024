import os
import json
from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    Text,
    DateTime,
    Date,
    text
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint
from utils import get_logger, get_db

OUTPUT_DIR = "./output"
script_base = os.path.splitext(os.path.basename(__file__))[0]
exercises_01_filename = os.path.join(OUTPUT_DIR, "exercises_01.json")
exercises_02_filename = os.path.join(OUTPUT_DIR, "exercises_02_candles.json")

log_filename = f"{script_base}.log"
logger = get_logger(log_filename=log_filename)

# Define the SQLAlchemy ORM base class
Base = declarative_base()

# ORM model for the executions table


class Execution(Base):
    __tablename__ = "executions"
    id = Column(BigInteger, nullable=False)
    side = Column(Text, nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    size = Column(Numeric(20, 8), nullable=False)
    exec_date = Column(DateTime(timezone=True), nullable=False)
    buy_child_order_acceptance_id = Column(Text)
    sell_child_order_acceptance_id = Column(Text)
    # This is a generated column in SQL, not used by ORM
    day = Column(Date, nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('id', 'exec_date', name='executions_pkey'),
    )

# ORM model for the candles table


class Candle(Base):
    __tablename__ = "candles"
    minute = Column(DateTime(timezone=True), primary_key=True)
    open = Column(Numeric(20, 8), nullable=False)
    high = Column(Numeric(20, 8), nullable=False)
    low = Column(Numeric(20, 8), nullable=False)
    close = Column(Numeric(20, 8), nullable=False)
    volume = Column(Numeric(20, 8), nullable=False)
    vwap = Column(Numeric(20, 8), nullable=False)
    # This is a generated column in SQL, not used by ORM
    day = Column(Date, nullable=False)


def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, "r") as f:
        return json.load(f)


def main():
    engine = get_db()

    # 1. Initialize database schema from SQL file
    try:
        logger.info("Reading SQL schema from exercises_03.sql")
        with open('exercises_03.sql', 'r') as f:
            sql_script = f.read()
        logger.info(
            f"Executing SQL script from exercises_03.sql: {sql_script[:100]}...")
        with engine.connect() as connection:
            for statement in sql_script.split(';'):
                stmt = statement.strip()
                if stmt:
                    logger.info(f"Executing SQL statement: {stmt[:80]}...")
                    connection.execute(text(stmt))
            connection.commit()
        logger.info(
            "✅ Database schema initialized from exercises_03.sql successfully.")
    except Exception as e:
        logger.error(
            f"❌ Error initializing database from exercises_03.sql: {e}")
        return

    # 2. Insert executions data from JSON file
    try:
        logger.info(f"Loading executions data from {exercises_01_filename}")
        executions = load_json(exercises_01_filename)
        logger.info(f"Loaded {len(executions)} executions records.")
        with engine.begin() as conn:
            for row in executions:
                exec_date = row["exec_date"]
                # Ensure exec_date has timezone info
                if "+" not in exec_date:
                    exec_date += "+00:00"
                logger.info(
                    f"Inserting execution id={row['id']} exec_date={exec_date}")
                conn.execute(
                    text("""
                        INSERT INTO executions (
                            id, side, price, size, exec_date,
                            buy_child_order_acceptance_id,
                            sell_child_order_acceptance_id
                        ) VALUES (
                            :id, :side, :price, :size, :exec_date,
                            :buy_child_order_acceptance_id,
                            :sell_child_order_acceptance_id
                        )
                        ON CONFLICT DO NOTHING
                    """),
                    {
                        "id": row["id"],
                        "side": row["side"],
                        "price": row["price"],
                        "size": row["size"],
                        "exec_date": exec_date,
                        "buy_child_order_acceptance_id": row.get("buy_child_order_acceptance_id"),
                        "sell_child_order_acceptance_id": row.get("sell_child_order_acceptance_id"),
                    }
                )
        logger.info("✅ Inserted executions data.")
    except Exception as e:
        logger.error(f"❌ Error inserting executions: {e}")

    # 3. Insert candles data from JSON file
    try:
        logger.info(f"Loading candles data from {exercises_02_filename}")
        candles = load_json(exercises_02_filename)
        logger.info(f"Loaded {len(candles)} candles records.")
        with engine.begin() as conn:
            for row in candles:
                logger.info(f"Inserting candle minute={row['minute']}")
                conn.execute(
                    text("""
                        INSERT INTO candles (
                            minute, open, high, low, close, volume, vwap
                        ) VALUES (
                            :minute, :open, :high, :low, :close, :volume, :vwap
                        )
                        ON CONFLICT DO NOTHING
                    """),
                    {
                        "minute": row["minute"],
                        "open": row["open"],
                        "high": row["high"],
                        "low": row["low"],
                        "close": row["close"],
                        "volume": row["volume"],
                        "vwap": row["vwap"],
                    }
                )
        logger.info("✅ Inserted candles data.")
    except Exception as e:
        logger.error(f"❌ Error inserting candles: {e}")

    print("--- Database Models Defined ---")
    print("Consider running 'psql -f exercises_03.sql' or similar to initialize the database with partitioning and indexes.")
    print("The Python models are for ORM mapping to an existing schema.")


if __name__ == "__main__":
    main()
