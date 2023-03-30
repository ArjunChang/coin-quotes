import json
from unittest import mock

import helpers
import pytest
from prices import run_task as run_prices_task
from quotes import run_task as run_quotes_task
from requests import Response
from requests.exceptions import RequestException


@pytest.fixture()
def database(postgresql):
    """Set up the mock DB with the SQL flat file."""
    with open("test.sql") as f:
        setup_sql = f.read()

    with postgresql.cursor() as cursor:
        cursor.execute(setup_sql)
        postgresql.commit()

    yield postgresql


def create_mock_response(status_code=200, data=b''):
    response = Response()
    response.status_code = status_code
    response._content = data
    return response


def test_format_quotes_response_data():
    test_data = {
        "data": {
            "btc_dominance": 67.0057,
            "eth_dominance": 9.02205,
            "quote": {
                "active_cryptocurrencies": 4986,
                "total_cryptocurrencies": 9607,
            }
        }
    }

    expected_result = {
        "btc_dominance": 67.0057,
        "eth_dominance": 9.02205,
        "quote": json.dumps({"active_cryptocurrencies": 4986, "total_cryptocurrencies": 9607})
    }

    result_data = helpers.format_quotes_response_data(test_data)

    assert result_data == expected_result


@mock.patch("helpers.get_db_connection")
@mock.patch("helpers.fetch_prices_response")
def test_insert_prices_data_success(mocked_response, mocked_connection, database):
    dummy_data = json.dumps([{
        'symbol': 'DUMMY',
        'price': 100,
        'time': 1680070347701
    }])
    mocked_response.return_value = create_mock_response(200, dummy_data.encode())
    mocked_connection.return_value = database

    run_prices_task()

    cursor = database.cursor()
    query = "SELECT * FROM DATA.FUTURES_PRICE;"
    cursor.execute(query)
    rows = cursor.fetchall()
    assert len(rows) == 1


@mock.patch("helpers.get_db_connection")
@mock.patch("helpers.fetch_prices_response")
def test_insert_prices_data_failure(mocked_response, mocked_connection, database):
    mocked_response.return_value = create_mock_response(400)
    mocked_connection.return_value = database

    with pytest.raises(RequestException):
        run_prices_task()


@mock.patch("helpers.get_db_connection")
@mock.patch("helpers.fetch_quotes_response")
def test_insert_quotes_data_success(mocked_response, mocked_connection, database):
    dummy_data = json.dumps({
        "data": {
            "quote": {
                "dummy": "data"
            },
            "derivatives_volume_24h_reported": 100
        }
    })
    mocked_response.return_value = create_mock_response(200, dummy_data.encode())
    mocked_connection.return_value = database

    run_quotes_task()

    cursor = database.cursor()
    query = "SELECT * FROM DATA.QUOTES;"
    cursor.execute(query)
    rows = cursor.fetchall()
    assert len(rows) == 1


@mock.patch("helpers.get_db_connection")
@mock.patch("helpers.fetch_quotes_response")
def test_insert_quotes_data_failure(mocked_response, mocked_connection, database):
    mocked_response.return_value = create_mock_response(400)
    mocked_connection.return_value = database

    with pytest.raises(RequestException):
        run_quotes_task()


@mock.patch("time.sleep")
def test_task_handler(mocked_sleep):
    mocked_sleep.return_value = None

    def dummy_function():
        raise RequestException("Dummy Exception")

    restart_count = helpers.task_handler(dummy_function)

    assert restart_count == 3
