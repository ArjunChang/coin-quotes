import json
import logging
from datetime import datetime

import helpers
import sentry_sdk
from requests.exceptions import RequestException
from setup import setup
from os import getenv


def run_task():
    logging.info(f"Querying Futures API at {datetime.now()}")
    response = helpers.fetch_prices_response()

    # Error handling
    if response.status_code != 200:
        raise RequestException(response=response)

    data = json.loads(response.text)

    # Connect to the DB
    conn = helpers.get_db_connection()

    # Format data to suit the DB Schema
    helpers.insert_prices_data(conn, data)
    logging.info(f"New entry inserted at {datetime.now()}")


if __name__ == "__main__":
    # Initiating sentry
    sentry_sdk.init(
        dsn=getenv("SENTRY_DSN"),
        traces_sample_rate=1.0
    )

    # Ensure database is setup
    setup()

    helpers.task_handler(run_task)
