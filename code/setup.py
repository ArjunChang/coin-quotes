from helpers import get_db_connection, get_logger
from datetime import datetime

logger = get_logger()


def setup():
    # Establishing the connection
    conn = get_db_connection()

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Doping EMPLOYEE table if already exists.
    cursor.execute("DROP TABLE IF EXISTS DATA")

    # Creating table as per requirement
    sql = """CREATE TABLE DATA(
        data_id serial primary key,
        active_cryptocurrencies integer,
        active_exchanges integer,
        active_market_pairs integer,
        btc_dominance numeric(7,4),
        btc_dominance_24h_percentage_change numeric(7,4),
        btc_dominance_yesterday numeric(7,4),
        defi_24h_percentage_change numeric(7,4),
        defi_market_cap numeric(16,4),
        defi_volume_24h numeric(16,4),
        defi_volume_24h_reported numeric(16,4),
        derivatives_24h_percentage_change numeric(7,4),
        derivatives_volume_24h numeric(16,4),
        derivatives_volume_24h_reported numeric(16,4),
        eth_dominance numeric(7,4),
        eth_dominance_24h_percentage_change numeric(7,4),
        eth_dominance_yesterday numeric(7,4),
        last_updated timestamp,
        quote json,
        stablecoin_24h_percentage_change numeric(7,4),
        stablecoin_market_cap numeric(16,4),
        stablecoin_volume_24h numeric(16,4),
        stablecoin_volume_24h_reported numeric(16,4),
        total_cryptocurrencies integer,
        total_exchanges integer
        )"""
    
    cursor.execute(sql)
    conn.commit()

    # Logging info
    logger.info(f"Table created successfully at {datetime.now()}")

    # Closing the connection
    conn.close()
