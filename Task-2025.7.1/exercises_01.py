import os
import time
import requests
import json
from utils import get_logger

OUTPUT_DIR = "./output"

# Configure logging to a file with the same base name as this script
script_base = os.path.splitext(os.path.basename(__file__))[0]
json_filename = os.path.join(OUTPUT_DIR, f"{script_base}.json")

log_filename = f"{script_base}.log"
logger = get_logger(log_filename=log_filename)

# bitFlyer execution API endpoint and configuration constants
API = "https://api.bitflyer.com/v1/getexecutions"
SLEEP_INTERVAL = 1.0           # Seconds between successful API calls
MAX_RETRIES = 5                # Maximum number of retry attempts on failure
BACKOFF_FACTOR = 2.0           # Exponential backoff multiplier for retry delays
GET_ALL = True                # If True, keep crawling until no more data
MAX_PAGE = 20               # Maximum number of pages to fetch (for testing)


def fetch_executions(product_code="BTC_JPY", count=100, before=None, after=None):
    """
    Fetch a page of executions from bitFlyer.
    Returns a tuple (data_list, next_before_id).
    """
    logger.info(
        f"Fetching executions for {product_code} (count={count}, before={before}, after={after})"
    )
    params = {"product_code": product_code, "count": count}
    if before is not None:
        params["before"] = before   # Page backward using 'before' id
    if after is not None:
        params["after"] = after     # Page forward using 'after' id

    logger.info(f"Requesting {API} with params: {params}")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Make HTTP GET request to bitFlyer API
            resp = requests.get(API, params=params, timeout=10)
            resp.raise_for_status()      # Raise for HTTP errors
            data = resp.json()          # Parse JSON response

            logger.info(
                f"Got {len(data)} executions (showing up to 3): {data[:3]}…"
            )
            for item in data:
                # Debug log each execution entry
                logger.debug(
                    f"{item['id']}: {item['side']} {item['size']} @ {item['price']} ({item['exec_date']})"
                )

            # Determine next 'before' cursor (smallest execution id) for pagination
            next_before = min(item["id"] for item in data) if data else None
            return data, next_before

        except Exception as e:
            # On error, wait with exponential backoff and retry
            wait = BACKOFF_FACTOR ** (attempt - 1)
            logger.warning(
                f"Attempt {attempt} failed: {e!r}; retrying in {wait:.1f}s…"
            )
            time.sleep(wait)

    # If all retries fail, log error and abort
    logger.error("Max retries exceeded, aborting fetch_executions")
    raise RuntimeError("Max retries exceeded")


def crawl_all():
    """
    Crawl executions until no more data (or only once if GET_ALL=False).
    Saves fetched executions to a JSON file with overwrite mode.
    """
    before = None
    all_data = []  # Accumulate executions if GET_ALL is True
    count = 0

    while count < MAX_PAGE:
        data, next_before = fetch_executions(before=before)
        if not data:
            logger.info("No more executions, exiting crawl.")
            break

        logger.info(
            f"Processed {len(data)} executions; next before={next_before}")
        all_data.extend(data)
        before = next_before
        time.sleep(SLEEP_INTERVAL)
        count += 1
        if not GET_ALL:
            # Only fetch one page if GET_ALL is False
            break

    # Overwrite JSON file with the latest list of executions
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved {len(all_data)} executions to {json_filename}")


if __name__ == "__main__":
    crawl_all()
