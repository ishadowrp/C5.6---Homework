#Импортируем библиотеку telebot и собственные модули config и extensions
import telebot
from config import TOKEN, keys
from extensions import CurrencyConverter, APIException

#Подключаем бот
bot = telebot.TeleBot(TOKEN)

#Создаем функцию помощи. При вводе в боте команды /start или /help будет выводится справка
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом необходимо ввести команду в следующем формате:\n<имя валюты из которой нужно совершить конвертацию> \
<валюта в которую нужно совершить конвертацию> \
<количество конвертируемой валюты>\n' \
           'Для вывода списка доступных валют из/в которые возможна конвертация, введите команду /values'

    bot.send_message(message.chat.id, text)

#Создадим функцию, которая при вводе команды /values будет выводить список доступных валют для конвертации
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#Создадим процедуру, которая будет обрабатывать сообщение пользователя и конвертировать валюту
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    #Для обработки исключений всю обработку обернем в try
    try:
        list_of_values = message.text.split(' ')

        if len(list_of_values) != 3:
            raise APIException('Не верное количество параметров.')

        base, quote, amount = list_of_values
        #Вызовем собственно саму обработку конвертации
        total_amount = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Упс.. Что-то пошло не так. Не удалось обработать команду\n{e}')
    else:
        #Если код в попытке (try) выполнился успешно - выведем пользователю полученную сумму
        text = f'Сумма после конвертации: {round(total_amount, 2)} {keys[quote]}'
        bot.reply_to(message, text)

#Запустим бота на выолнение
bot.polling()
