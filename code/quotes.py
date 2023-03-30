import json
import logging
from datetime import datetime

import helpers
import sentry_sdk
from requests.exceptions import RequestException
from setup import setup
from os import getenv


def run_task():
    logging.info(f"Querying API at {datetime.now()}")
    response = helpers.fetch_quotes_response()

    # Error handling
    if response.status_code != 200:
        raise RequestException(response=response)

    data = json.loads(response.text)

    # Connect to the DB
    conn = helpers.get_db_connection()

    # Format data to suit the DB Schema
    formatted_data = helpers.format_quotes_response_data(data)
    helpers.insert_quotes_data(conn, **formatted_data)
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
