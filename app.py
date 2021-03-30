import telebot
from config import TOKEN, keys
from extension import CurrencyConverter, APIException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом необходимо ввести команду в следующем формате:\n<имя валюты из которой нужно совершить конвертацию> \
<валюта в которую нужно совершить конвертацию> \
<количество конвертируемой валюты>\n' \
           'Для вывода списка доступных валют из/в которые возможна конвертация, введите команду /values'

    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        list_of_values = message.text.split(' ')

        if len(list_of_values) != 3:
            raise APIException('Не верное количество параметров.')

        base, quote, amount = list_of_values
        total_amount = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Упс.. Что-то пошло не так. Не удалось обработать команду\n{e}')
    else:
        text = f'Сумма конвертации: {round(total_amount, 2)} {quote}'
        bot.reply_to(message, text)

bot.polling()
