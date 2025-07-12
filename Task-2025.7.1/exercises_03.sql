-- exercises_03.sql

-- ===============================================================
-- 1. Create & partition the executions table
-- ===============================================================

-- Drop existing table (and all child partitions) if any
DROP TABLE IF EXISTS executions CASCADE;

-- Create parent table for executions, partitioned by exec_date
CREATE TABLE executions (
    id                  BIGINT            NOT NULL,
    side                TEXT              NOT NULL CHECK (side IN ('BUY','SELL')),
    price               NUMERIC(20,8)     NOT NULL,
    size                NUMERIC(20,8)     NOT NULL,
    exec_date           TIMESTAMPTZ       NOT NULL,
    buy_child_order_acceptance_id  TEXT,
    sell_child_order_acceptance_id TEXT,

    -- Persisted UTC date for each execution, to speed up daily grouping
    day DATE GENERATED ALWAYS AS ((exec_date AT TIME ZONE 'UTC')::date) STORED,

    PRIMARY KEY (id, exec_date)
) PARTITION BY RANGE (exec_date);

-- Create a partition for June 2025
-- (In production you would script creation of each future partition)
CREATE TABLE IF NOT EXISTS executions_2025_06
  PARTITION OF executions
  FOR VALUES FROM ('2025-06-01 00:00:00+00') TO ('2025-07-01 00:00:00+00');

-- ===============================================================
-- 1.1 Indexes on executions
-- ===============================================================

-- Index on exec_date for fast time-based queries
CREATE INDEX IF NOT EXISTS idx_executions_exec_date
  ON executions(exec_date);

-- Composite index on day + price for fast daily + price‐filtered aggregations
CREATE INDEX IF NOT EXISTS idx_executions_day_price
  ON executions(day, price);




-- ===============================================================
-- 2. Create the candles table
-- ===============================================================

-- Drop existing table if any
DROP TABLE IF EXISTS candles;

-- Create candles table
CREATE TABLE candles (
    minute TIMESTAMPTZ    NOT NULL PRIMARY KEY,   -- aggregation window (to the minute)
    open   NUMERIC(20,8)  NOT NULL,               -- open price
    high   NUMERIC(20,8)  NOT NULL,               -- highest price
    low    NUMERIC(20,8)  NOT NULL,               -- lowest price
    close  NUMERIC(20,8)  NOT NULL,               -- close price
    volume NUMERIC(20,8)  NOT NULL,               -- total volume
    vwap   NUMERIC(20,8)  NOT NULL,               -- volume‐weighted avg. price

    -- Persisted UTC date for each candle, to speed up daily grouping
    day DATE GENERATED ALWAYS AS ((minute AT TIME ZONE 'UTC')::date) STORED
);

-- ===============================================================
-- 2.1 Index on candles.day
-- ===============================================================

-- Speed up queries grouped by day
CREATE INDEX IF NOT EXISTS idx_candles_day
  ON candles(day);
