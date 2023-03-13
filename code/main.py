import json
import logging
from datetime import datetime
from time import sleep

from requests.exceptions import RequestException

from helpers import format_response_data, get_db_connection, get_session, insert_data

logging.basicConfig(
    filename="std.log", filemode="a", format="%(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def run_task():
    # Setup the session
    session = get_session()
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"

    while True:
        try:
            logger.info(f"Querying API at {datetime.now()}")
            response = session.get(url)

            if response.status_code != 200:
                raise RequestException(response)

            data = json.loads(response.text)

            # Connect to the DB
            conn = get_db_connection()

            # Format data to suit the DB Schema
            formatted_data = format_response_data(data)
            insert_data(conn, **formatted_data)
            logger.info(f"New entry inserted at {datetime.now()}")
            conn.close()

            # Wait for 5min before querying the api again
            sleep(300)

        except RequestException as e:
            # Log the error
            logger.error(e)


if __name__ == "__main__":
    run_task()
