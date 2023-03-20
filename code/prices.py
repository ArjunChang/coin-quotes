import json
import logging
from datetime import datetime
from time import sleep

import sentry_sdk
from helpers import get_db_connection, insert_prices_data
from requests import Session
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
    session = Session()
    url = "https://fapi.binance.com/fapi/v1/ticker/price"

    try:
        logging.info(f"Querying Futures API at {datetime.now()}")
        response = session.get(url)

        # Error handling
        if response.status_code != 200:
            raise RequestException(response=response)

        data = json.loads(response.text)

        # Connect to the DB
        conn = get_db_connection()

        # Format data to suit the DB Schema
        insert_prices_data(conn, data)
        logging.info(f"New entry inserted at {datetime.now()}")
        print("Inserted")

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
