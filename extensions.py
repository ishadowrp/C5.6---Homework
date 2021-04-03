#Импортируем библиотеки requests и json и наш конфигурационный файл
import requests
import json
from config import keys

#Создадим клас-исключение
class APIException(Exception):
    pass

#Создадим клас конвертации валюты со статичным методом get_price
class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        #Так как в словаре валют все названия валют написаны маленькими буквами приведем введеные пользователем
        #наименования валют были тоже в нижмнем регистре
        base = base.lower()
        quote = quote.lower()

        #Проверим одинаковая ли валюта из которой идет конвертация в котороую и если это так поднимем исключение
        if base == quote:
            raise APIException(f'Невозможно провести конвертацию из одной и той же валюты: {base}')
        #Проверим есть ли в списке валюта, которую пользователь желает сконвертировать, если нет вызовем исключение
        try:
            base_str = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        #Проверим есть ли в списке валюта, в которую пользователь желает сконвертировать, если нет вызовем исключение
        try:
            symbols_str = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        #Проверим является ли числовым значение введенная пользователем сумма для конвертации, в противном случае вызовем исключение
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму для конвертации: {amount}')

        #Получим курс валюты по API
        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={base_str}&symbols={symbols_str}')
        #Вернем сконвертированную сумму
        return float(json.loads((r.content))['rates'][keys[quote]])*amount
