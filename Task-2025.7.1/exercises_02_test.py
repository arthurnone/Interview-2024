import json
from datetime import datetime, timezone
import pytest

# adjust this import to match your script filename (without .py)
from exercises_02 import (
    Execution,
    Candle,
    load_executions_from_json,
    aggregate_to_candles,
    save_candles_to_json,
)


SAMPLE_EXEC_JSON = [
    {
        "id": 1,
        "side": "BUY",
        "price": 100.0,
        "size": 1.0,
        "exec_date": "2025-06-09T11:10:10.000",  # treated as UTC
    },
    {
        "id": 2,
        "side": "SELL",
        "price": 110.0,
        "size": 2.0,
        "exec_date": "2025-06-09T11:10:50.000",
    },
    {
        "id": 3,
        "side": "BUY",
        "price": 120.0,
        "size": 1.5,
        "exec_date": "2025-06-09T11:11:05.000",
    },
]


@pytest.fixture
def sample_json_file(tmp_path):
    p = tmp_path / "sample_exec.json"
    p.write_text(json.dumps(SAMPLE_EXEC_JSON, ensure_ascii=False, indent=2))
    return str(p)


def test_load_executions_from_json(sample_json_file):
    execs = load_executions_from_json(sample_json_file)
    # should load exactly as many items as in SAMPLE_EXEC_JSON
    assert len(execs) == len(SAMPLE_EXEC_JSON)

    # check one of them
    first = execs[0]
    assert isinstance(first, Execution)
    assert first.id == SAMPLE_EXEC_JSON[0]["id"]
    assert first.price == pytest.approx(SAMPLE_EXEC_JSON[0]["price"])
    assert first.size == pytest.approx(SAMPLE_EXEC_JSON[0]["size"])
    # timestamp should be parsed and timezone‐aware
    expect_ts = datetime.fromisoformat(SAMPLE_EXEC_JSON[0]["exec_date"])
    if expect_ts.tzinfo is None:
        expect_ts = expect_ts.replace(tzinfo=timezone.utc)
    assert first.timestamp == expect_ts


def test_aggregate_to_candles():
    # prepare three Execution objects in two distinct minutes
    execs = [
        Execution(1, 100.0, 1.0, datetime(
            2025, 6, 9, 11, 10, 10, tzinfo=timezone.utc)),
        Execution(2, 110.0, 2.0, datetime(
            2025, 6, 9, 11, 10, 50, tzinfo=timezone.utc)),
        Execution(3, 120.0, 1.5, datetime(
            2025, 6, 9, 11, 11, 5, tzinfo=timezone.utc)),
    ]
    # use an artificial last_close
    candles = aggregate_to_candles(execs, last_close=90.0)

    # should have two minutes: 11:10 and 11:11
    minutes = sorted(candles.keys())
    assert minutes == [
        datetime(2025, 6, 9, 11, 10, tzinfo=timezone.utc),
        datetime(2025, 6, 9, 11, 11, tzinfo=timezone.utc),
    ]

    c1 = candles[minutes[0]]
    assert isinstance(c1, Candle)
    # minute 11:10: open=100, high=110, low=100, close=110, volume=3.0, vwap=(100*1+110*2)/3
    assert c1.open == 100.0
    assert c1.high == 110.0
    assert c1.low == 100.0
    assert c1.close == 110.0
    assert c1.volume == pytest.approx(3.0)
    assert c1.vwap == pytest.approx((100*1 + 110*2) / 3)

    c2 = candles[minutes[1]]
    # minute 11:11: only one trade
    assert c2.open == 120.0
    assert c2.high == 120.0
    assert c2.low == 120.0
    assert c2.close == 120.0
    assert c2.volume == pytest.approx(1.5)
    assert c2.vwap == pytest.approx(120.0)


def test_save_candles_to_json(tmp_path):
    # create a single candle for testing
    m = datetime(2025, 6, 9, 11, 10, tzinfo=timezone.utc)
    candle = Candle(m, open=100, high=110, low=90,
                    close=105, volume=3.0, vwap=105.0)
    out_file = tmp_path / "out_candles.json"

    save_candles_to_json({m: candle}, str(out_file))

    # read it back and verify structure
    data = json.loads(out_file.read_text())
    assert isinstance(data, list) and len(data) == 1

    entry = data[0]
    assert entry["minute"] == "2025-06-09T11:10:00+00:00"
    assert entry["open"] == 100
    assert entry["high"] == 110
    assert entry["low"] == 90
    assert entry["close"] == 105
    assert entry["volume"] == 3.0
    assert entry["vwap"] == 105.0
