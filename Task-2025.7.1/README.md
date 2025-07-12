# Pafin Assignment – Solution Guide

## Assignment Files Overview

### Exercises 1

#### **exercises_01.py**

> **Q1: Explain concisely how you would fetch the data from bitflyer.**

- Implements a Python script that fetches executions data from BitFlyer’s `getexecutions` API endpoint.
- Uses the `requests` library with robust logging (writes to `log/exercises_01.log`).
- Stores the fetched executions as a JSON file (`output/exercises_01.json`) for use in later steps.
- The script is configurable: you can set the API endpoint, retry policy (with exponential backoff), pagination, and sleep intervals.

#### **exercises_01.json**

- Stores the raw executions data fetched by `exercises_01.py`.
- Used as the input fixture for Exercise 2.

---

### Exercises 2

#### **exercises_02.py**

> **Q2: Define the data structures you would use for executions and candles and write functions to process executions and build candles.**

- Defines two `@dataclass`es: `Execution` and `Candle`.
- Implements:
  - `load_executions_from_json(...)`: parses raw JSON into a list of `Execution` objects.
  - `aggregate_to_candles(...)`: groups executions by minute and computes OHLCV and VWAP values.
  - `save_candles_to_json(...)`: writes the resulting candles to JSON for downstream use or testing.

#### **exercises_02_test.py**

- A `pytest`-style test suite that covers:
  - Loading a sample of execution records.
  - Aggregating executions to candles and verifying correctness of OHLCV/VWAP.
  - Edge cases (e.g., missing data, empty minutes).

#### **exercises_02_candle.py** _(Reference Only)_

- Extra script that visualizes the candle data:
  - Reads candles JSON from `exercises_02.py`.
  - Uses `matplotlib` to render and save a 1-minute candlestick chart (`output/exercises_02_candles.png`).
  - Provided for reference only—no changes required.

#### **exercises_02_candles.json**

- Output: Aggregated candles data computed from executions.

#### **exercises_02_candles.png**

- Candlestick chart generated from the candles data.

---

### Exercises 3

#### **exercises_03.sql**

> **Q3: Suggest a PostgreSQL schema and SQL queries to store the executions and candles.**

- Contains a complete PostgreSQL schema:
  - `executions` table, partitioned by `exec_date` for efficient time-based queries.
  - `candles` table for storing 1-minute aggregates.
  - Proper indexes and `GENERATED ALWAYS AS` columns for analytics.
- Designed to support efficient time-series queries and data integrity.

#### **exercises_03.py**

- Provides SQLAlchemy ORM models for the above schema.
- Reads and executes the schema from `exercises_03.sql` to fully initialize PostgreSQL, including partitions and generated columns.
- Loads sample executions/candles data from JSON files and inserts into the database.
- All database operations are logged to `log/exercises_03.log`.
- The ORM is used for convenient interaction, while advanced schema features are defined via SQL.

#### **docker-compose.yml**

- Orchestrates a reproducible development environment with PostgreSQL and Python services.
- Ensures the schema is initialized before Python attempts data import or query.

---

### Exercises 4

#### **exercises_04.py**

> **Q4: Suggest efficient SQL queries to handle the following:**  
> **4.1. Find the daily minimum and maximum price over the last 30 days**  
> **4.2. Find the daily volume of executions that happened over and under a given price (parameter) for the last 30 days**

- Implements a FastAPI web service that exposes efficient SQL queries for trading analytics.
- Provides two endpoints:
  - `/daily-high-low`: Returns daily min and max price for the last 30 days (from the `executions` table).
  - `/daily-volume-by-price`: Given a price, returns daily execution volume above and below that price for the last 30 days.
- Uses parameterized SQL for safety and efficiency.
- All API requests and database queries are logged to `log/exercises_04.log`.

---

## Other Files

- **requirements.txt**  
  Lists all dependencies required for the exercises.

- **docker-compose.yml**  
  (See above; used for Exercises 3 and 4.)

- **utils.py**  
  Shared utility code:
  - Initializes `log/` and `output/` directories.
  - Configures loggers for all scripts.
  - Sets up PostgreSQL database connections.

---

## Logging and Output

- Each Python script creates a detailed log file under `log/` (e.g., `exercises_01.log`), capturing all key operations, errors, and debug information.
- All major data files and visual outputs are placed in the `output/` directory for easy review and validation.

---

## How to Run

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **For database-related exercises, use Docker Compose:**

   ```bash
   docker-compose up
   ```

3. **Run each script as needed.**
   Log files will be found in `log/`, and data/figures in `output/`.
