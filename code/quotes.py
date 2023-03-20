import json
import logging
from datetime import datetime
from time import sleep

import sentry_sdk
from helpers import (format_quotes_response_data, get_db_connection,
                     get_quotes_session, insert_quotes_data)
from requests.exceptions import RequestException
from setup import setup

# Initiating sentry
sentry_sdk.init(
    dsn="https://045d2c17a4984779ae2cb6bf045cf625@o4504849798397952.ingest.sentry.io/4504871620116480",
    traces_sample_rate=1.0
)


def run_task():
    # Inititiate backoff time
    CURRENT_BACKOFF_TIME = 10

    # Setup the session
    session = get_quotes_session()
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"

    try:
        logging.info(f"Querying API at {datetime.now()}")
        response = session.get(url)

        # Error handling
        if response.status_code != 200:
            raise RequestException(response=response)

        data = json.loads(response.text)

        # Connect to the DB
        conn = get_db_connection()

        # Format data to suit the DB Schema
        formatted_data = format_quotes_response_data(data)
        insert_quotes_data(conn, **formatted_data)
        logging.info(f"New entry inserted at {datetime.now()}")

        # Close DB connection
        conn.close()

        # Reset backoff time
        CURRENT_BACKOFF_TIME = 10

    except RequestException as e:
        # Log the error
        logging.error(e)

        # Wait for a while and set backoff time
        sleep(CURRENT_BACKOFF_TIME)
        CURRENT_BACKOFF_TIME *= 2


if __name__ == "__main__":
    setup()
    run_task()
