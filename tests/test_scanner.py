import asyncio
import pytest
from aioresponses import aioresponses

from scanner import Currency, Scanner


@pytest.mark.asyncio
async def test_do_one_request():
    # Create a dummy scanner object for testing
    scanner = Scanner([])

    # Create a dummy currency object for testing
    currency = Currency("BTC", 'text_for_wrong_url')

    # Create an asyncio.Queue instance for testing
    queue = asyncio.Queue()

    # Mock the response JSON
    response_json = {
        "result": {
            "index_price": 50000.0
        }
    }

    # Set up aioresponses to mock the HTTP request
    with aioresponses() as mock_response:
        # Mock the response for the specific URL
        mock_response.get(currency.create_index_url(), status=200, payload=response_json)

        # Call the method under test
        await scanner._do_one_request(currency, queue)

    # Perform assertions on the contents of the queue
    assert queue.qsize() == 1
    result = await queue.get()
    assert result["ticker"] == "BTC"
    assert result["price"] == 5000000  # 50000 * 100
    assert "timestamp" in result
