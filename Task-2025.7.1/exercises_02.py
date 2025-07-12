import os
import json
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import List, Dict
from utils import get_logger

OUTPUT_DIR = "./output"

script_base = os.path.splitext(os.path.basename(__file__))[0]
json_filename = os.path.join(OUTPUT_DIR, "exercises_01.json")
candles_filename = os.path.join(
    OUTPUT_DIR, f"{script_base}_candles.json")  # Output candles JSON
image_filename = os.path.join(
    OUTPUT_DIR, f"{script_base}_candles.png")  # Output image file

log_filename = f"{script_base}.log"
logger = get_logger(log_filename=log_filename)


@dataclass
class Execution:
    id: int
    price: float
    size: float
    timestamp: datetime


@dataclass
class Candle:
    minute: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float


def load_executions_from_json(file_path: str) -> List[Execution]:
    """
    Load raw execution JSON data and convert to a list of Execution objects.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    execs: List[Execution] = []
    for item in raw:
        ts = datetime.fromisoformat(item['exec_date'])
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        execs.append(Execution(
            id=item['id'],
            price=item['price'],
            size=item['size'],
            timestamp=ts
        ))
    logger.info(f"Loaded {len(execs)} executions from {file_path}")
    return execs


def aggregate_to_candles(execs: List[Execution], last_close: float) -> Dict[datetime, Candle]:
    """
    Group executions by minute and build a Candle for each minute.
    """
    from collections import defaultdict
    buckets: Dict[datetime, List[Execution]] = defaultdict(list)
    for ex in execs:
        minute = ex.timestamp.replace(second=0, microsecond=0)
        buckets[minute].append(ex)

    result: Dict[datetime, Candle] = {}
    for minute in sorted(buckets):
        group = buckets[minute]
        if group:
            prices = [e.price for e in group]
            sizes = [e.size for e in group]
            o = group[0].price
            c = group[-1].price
            h = max(prices)
            l = min(prices)
            v = sum(sizes)
            vw = sum(p * s for p, s in zip(prices, sizes)) / v
        else:
            o = h = l = c = last_close
            v = 0
            vw = last_close
        candle = Candle(minute, o, h, l, c, v, vw)
        result[minute] = candle
        last_close = candle.close
    logger.info(f"Aggregated into {len(result)} candles")
    return result


def save_candles_to_json(candles: Dict[datetime, Candle], file_path: str):
    """
    Save candles dict to JSON file, serializing datetimes to ISO strings.
    """
    out = []
    for minute, c in candles.items():
        out.append({
            'minute': minute.isoformat(),
            'open': c.open,
            'high': c.high,
            'low': c.low,
            'close': c.close,
            'volume': c.volume,
            'vwap': c.vwap
        })
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(out)} candles to {file_path}")


def main():
    # Load raw executions from JSON
    execs = load_executions_from_json(json_filename)

    # Determine initial last_close as the first execution price
    initial_close = execs[0].price if execs else 0.0

    # Aggregate into 1-minute candles
    candles = aggregate_to_candles(execs, last_close=initial_close)

    # Save candles to JSON for tests
    save_candles_to_json(candles, candles_filename)


if __name__ == '__main__':
    main()
