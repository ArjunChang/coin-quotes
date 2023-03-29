import json
import logging
from datetime import datetime
from time import sleep

import sentry_sdk
import helpers
from requests.exceptions import RequestException
from setup import setup

# Initiating sentry
sentry_sdk.init(
    dsn="https://045d2c17a4984779ae2cb6bf045cf625@o4504849798397952.ingest.sentry.io/4504871620116480",
    traces_sample_rate=1.0
)


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
    setup()

    # Inititiate backoff time and restart count
    RESTART_COUNT = 1
    CURRENT_BACKOFF_TIME = 10

    while RESTART_COUNT <= 3:
        try:
            run_task()
            
            # Reset backoff time and exit loop
            CURRENT_BACKOFF_TIME = 10
            break

        except RequestException as e:
            RESTART_COUNT += 1
            # Log the error when error is encountered thrice
            if RESTART_COUNT == 3:
                logging.error(e)

            # Wait for a while and set backoff time
            sleep(CURRENT_BACKOFF_TIME)
            CURRENT_BACKOFF_TIME *= 2
