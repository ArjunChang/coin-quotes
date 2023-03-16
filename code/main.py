import json
import logging
from datetime import datetime

from requests.exceptions import RequestException

from helpers import (
    format_response_data,
    get_db_connection,
    get_session,
    insert_data,
)
from setup import setup


def run_task():
    # Setup the session
    session = get_session()
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"

    try:
        logging.info(f"Querying API at {datetime.now()}")
        response = session.get(url)

        # Error handling
        if response.status_code != 200:
            raise RequestException(response)

        data = json.loads(response.text)

        # Connect to the DB
        conn = get_db_connection()

        # Format data to suit the DB Schema
        formatted_data = format_response_data(data)
        insert_data(conn, **formatted_data)
        logging.info(f"New entry inserted at {datetime.now()}")

        # Close DB connection
        conn.close()

    except RequestException as e:
        # Log the error
        logging.error(e)


if __name__ == "__main__":
    setup()
    run_task()
