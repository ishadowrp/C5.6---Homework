import requests
import json
from config import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Невозможно провести конвертацию из одной и той же валюты: {base}')

        try:
            base_str = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            symbols_str = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму для конвертации: {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={base_str}&symbols={symbols_str}')
        return float(json.loads((r.content))['rates'][keys[quote]])*amount
