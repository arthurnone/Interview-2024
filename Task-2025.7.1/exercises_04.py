import os
from fastapi import FastAPI, Query
from utils import get_db, get_logger
from sqlalchemy import text

script_base = os.path.splitext(os.path.basename(__file__))[0]
log_filename = f"{script_base}.log"
logger = get_logger(log_filename=log_filename)

app = FastAPI()
engine = get_db()


@app.get("/daily-high-low")
def daily_high_low():
    """
    Get the highest and lowest price for each day in the last 30 days.
    """
    logger.info("Request received: /daily-high-low")
    with engine.connect() as conn:
        sql = """
            SELECT
                day,
                MAX(price) AS high,
                MIN(price) AS low
            FROM executions
            WHERE day >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY day
            ORDER BY day DESC
        """
        logger.info("Executing SQL for daily high/low prices")
        result = conn.execute(text(sql))
        data = [
            {"day": str(row.day), "high": float(
                row.high), "low": float(row.low)}
            for row in result
        ]
    logger.info(f"Returning {len(data)} records for /daily-high-low")
    return {"data": data}


@app.get("/daily-volume-by-price")
def daily_volume_by_price(price: float = Query(..., description="The price threshold")):
    """
    Get daily volume above and below a given price for the last 30 days.
    """
    logger.info(f"Request received: /daily-volume-by-price?price={price}")
    with engine.connect() as conn:
        sql = """
            SELECT
                day,
                SUM(CASE WHEN price >= :price THEN size ELSE 0 END) AS volume_above,
                SUM(CASE WHEN price < :price THEN size ELSE 0 END) AS volume_below
            FROM executions
            WHERE day >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY day
            ORDER BY day DESC
        """
        logger.info("Executing SQL for daily volume by price")
        result = conn.execute(text(sql), {"price": price})
        data = [
            {
                "day": str(row.day),
                "volume_above": float(row.volume_above),
                "volume_below": float(row.volume_below)
            }
            for row in result
        ]
    logger.info(f"Returning {len(data)} records for /daily-volume-by-price")
    return {"data": data}

# To run with custom port and debug, use:
# uvicorn exercises_04:app --reload --port 8080
