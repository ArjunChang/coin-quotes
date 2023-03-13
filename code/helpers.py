from psycopg2._psycopg import connection
from psycopg2 import connect
import json
from requests import Session
import logging


def get_logger():
    logging.basicConfig(
        filename="task_logs.log",
        filemode="a",
        format="%(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger


def get_db_connection(
    database: str = "coinDB",
    user: str = "postgres",
    password: str = "sunnyside10",
    host: str = "127.0.0.1",
    port: str = "5432",
):
    conn = connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port,
    )

    return conn


def get_session() -> Session:
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "9f4f9d88-3032-4457-9f7d-d4e597df7819",
    }

    session = Session()
    session.headers.update(headers)
    return session


def format_response_data(data: dict) -> str:
    formated_data = data["data"]
    formated_data["quote"] = json.dumps(formated_data["quote"])
    return formated_data


def insert_data(
    conn: connection,
    active_cryptocurrencies: int = None,
    active_exchanges: int = None,
    active_market_pairs: int = None,
    btc_dominance: float = None,
    btc_dominance_24h_percentage_change: float = None,
    btc_dominance_yesterday: float = None,
    defi_24h_percentage_change: float = None,
    defi_market_cap: float = None,
    defi_volume_24h: float = None,
    defi_volume_24h_reported: float = None,
    derivatives_24h_percentage_change: float = None,
    derivatives_volume_24h: float = None,
    derivatives_volume_24h_reported: float = None,
    eth_dominance: float = None,
    eth_dominance_24h_percentage_change: float = None,
    eth_dominance_yesterday: float = None,
    last_updated: str = None,
    quote: dict = None,
    stablecoin_24h_percentage_change: float = None,
    stablecoin_market_cap: float = None,
    stablecoin_volume_24h: float = None,
    stablecoin_volume_24h_reported: float = None,
    total_cryptocurrencies: int = None,
    total_exchanges: int = None,
    *_
):
    """
    Insert data from api response into the database
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO data
        (active_cryptocurrencies, active_exchanges, active_market_pairs, btc_dominance,
        btc_dominance_24h_percentage_change, btc_dominance_yesterday, defi_24h_percentage_change,
        defi_market_cap, defi_volume_24h, defi_volume_24h_reported, derivatives_24h_percentage_change,
        derivatives_volume_24h, derivatives_volume_24h_reported, eth_dominance,
        eth_dominance_24h_percentage_change, eth_dominance_yesterday, last_updated, quote,
        stablecoin_24h_percentage_change, stablecoin_market_cap, stablecoin_volume_24h,
        stablecoin_volume_24h_reported, total_cryptocurrencies, total_exchanges) values
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            active_cryptocurrencies,
            active_exchanges,
            active_market_pairs,
            btc_dominance,
            btc_dominance_24h_percentage_change,
            btc_dominance_yesterday,
            defi_24h_percentage_change,
            defi_market_cap,
            defi_volume_24h,
            defi_volume_24h_reported,
            derivatives_24h_percentage_change,
            derivatives_volume_24h,
            derivatives_volume_24h_reported,
            eth_dominance,
            eth_dominance_24h_percentage_change,
            eth_dominance_yesterday,
            last_updated,
            quote,
            stablecoin_24h_percentage_change,
            stablecoin_market_cap,
            stablecoin_volume_24h,
            stablecoin_volume_24h_reported,
            total_cryptocurrencies,
            total_exchanges,
        ),
    )

    conn.commit()
