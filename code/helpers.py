import json
import logging
from datetime import datetime
from os import getenv

from psycopg2 import OperationalError, connect
from psycopg2._psycopg import connection
from requests import Session


def get_db_connection():
    try:
        conn = connect(
            database=getenv("POSTGRES_DB"),
            user=getenv("POSTGRES_USER"),
            password=getenv("POSTGRES_PASSWORD"),
            host=getenv("POSTGRES_HOST"),
            port=getenv("POSTGRES_PORT"),
        )

        return conn

    except OperationalError as e:
        logging.error(e)


def get_quotes_session() -> Session:
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": getenv("API_KEY"),
    }

    session = Session()
    session.headers.update(headers)
    return session


def fetch_quotes_response():
    session = get_quotes_session()
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    response = session.get(url)
    return response


def format_quotes_response_data(data: dict) -> str:
    formated_data = data["data"]
    formated_data["quote"] = json.dumps(formated_data["quote"])
    return formated_data


def fetch_prices_response():
    session = Session()
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    response = session.get(url)
    return response


def insert_prices_data(conn: connection, data: list = []):
    insert_statement = """INSERT INTO DATA.FUTURES_PRICE
    (symbol, price, transaction_time) VALUES
    """
    for row in data:
        date = datetime.fromtimestamp(row['time']/1000.0)
        insert_statement += f" ('{row['symbol']}', {row['price']}, '{date}'),"

    cursor = conn.cursor()
    cursor.execute(insert_statement[:-1])
    conn.commit()


def insert_quotes_data(
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
        INSERT INTO DATA.QUOTES
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
