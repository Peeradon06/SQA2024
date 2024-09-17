import unittest
from io import BytesIO

from requests.models import Response
from unittest.mock import patch
from assignment.source.currency_exchanger import CurrencyExchanger


def get_mock_country_api_response():
    mock_api_response = Response()
    mock_api_response.status_code = 200

    mock_api_response.raw = BytesIO(b'{ "base":"THB", "result":{"KRW":38.69}}')

    return mock_api_response

class TestCurrencyExchanger(unittest.TestCase):
    def setUp(self):
        self.currency_exchanger = CurrencyExchanger(base_currency="THB", target_currency="KRW")
        self.mock_api_response = get_mock_country_api_response()

    @patch("assignment.source.currency_exchanger.requests")
    def test_get_currency_rate(self, mock_request):

        # Arrange
        mock_request.get.return_value = self.mock_api_response

        # Act
        self.currency_exchanger.get_currency_rate()

        # Assert
        mock_request.get.assert_called_once()
        mock_request.get.assert_called_with("https://coc-kku-bank.com/foreign-exchange",
                                            params={'from': 'THB', 'to': 'KRW'})
        self.assertIsNotNone(self.currency_exchanger.api_response)
        self.assertEqual(self.mock_api_response.json(), self.currency_exchanger.api_response)


    @patch("assignment.source.currency_exchanger.requests")
    def test_currency_exchange(self, mock_request):
        # Arrange
        mock_request.get.return_value = self.mock_api_response
        thb_amount = 500
        expected_result = 19345.0   # THB -> KRW = 500 * 38.69 = 19345.0

        # Act
        exchange_result = self.currency_exchanger.currency_exchange(thb_amount)

        # Assert
        mock_request.get.assert_called_once()
        self.assertEqual(expected_result, exchange_result)
