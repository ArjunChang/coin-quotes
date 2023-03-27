from helpers import format_quotes_response_data
import json

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

    result_data = format_quotes_response_data(test_data)

    assert result_data == expected_result
