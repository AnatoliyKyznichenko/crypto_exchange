import telebot
from py_currency_converter import convert
from auth_data import token
from pycoingecko import CoinGeckoAPI
from telebot import types

cg = CoinGeckoAPI()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def main(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton("Получить курс криптовалюты"), types.KeyboardButton("Получить курс Фиата"))
    crypto = bot.send_message(message.chat.id, "Вы на главной", reply_markup=button)
    bot.register_next_step_handler(crypto,step)


def step(message):
    if message.text == "Получить курс криптовалюты":
        step2(message)
    elif message.text == "Получить курс Фиата":
        fiat(message)

def fiat(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton("USD"), types.KeyboardButton("UAH"), types.KeyboardButton("Вернуться на главную"))
    go_bot_fiat = bot.send_message(message.chat.id, "Курс Фиата", reply_markup=button)
    bot.register_next_step_handler(go_bot_fiat, fiat_step_2)


def fiat_step_2(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton("Назад"))
    if message.text == "USD":
        price = convert(base='USD', amount=1, to=['UAH', 'EUR'])
        bot.send_message(message.chat.id, f'1 USD : {price["UAH"]} UAH\n'
                                          f'1 USD : {price["EUR"]} EUR')

        go_main = bot.send_message(message.chat.id, "Вернуться назад?", reply_markup=button)
        bot.register_next_step_handler(go_main, fiat)

    elif message.text == "UAH":
        price = convert(base='UAH', amount=1, to=['USD', 'EUR'])
        bot.send_message(message.chat.id, f'1 UAH : {price["USD"]} USD\n'
                                          f'1 UAH : {price["EUR"]} EUR')

        go_main = bot.send_message(message.chat.id, "Вернуться назад?", reply_markup=button)
        bot.register_next_step_handler(go_main, fiat)

    elif message.text == "Вернуться на главную":
        main(message)


def step2(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton("Курс к USD"), types.KeyboardButton("Курс к UAH"), types.KeyboardButton("Главная"))
    go_bot_message = bot.send_message(message.chat.id, "Курс Токенов", reply_markup=button)
    bot.register_next_step_handler(go_bot_message, step3)


def step3(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton("Назад"))
    if message.text == "Курс к USD":
        price = cg.get_price(ids='bitcoin, ethereum, matic-network, uniswap', vs_currencies='usd')
        bot.send_message(message.chat.id, f'Цена токеннов:\n\n'
                                        f'Bitcoin price is {price["bitcoin"]["usd"]} $\n'
                                        f'Ethereum price is {price["ethereum"]["usd"]} $\n'
                                        f'Polygon price is {price["matic-network"]["usd"]} $\n'
                                        f'Uniswap price is {price["uniswap"]["usd"]} $\n', reply_markup=button)
        go_main = bot.send_message(message.chat.id, "Вернуться назад?", reply_markup=button)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == "Курс к UAH":
        price = cg.get_price(ids='bitcoin, ethereum, matic-network, uniswap', vs_currencies='uah')
        bot.send_message(message.chat.id, f'Цена токеннов:\n\n'
                                        f'Bitcoin price is {price["bitcoin"]["uah"]} UAH\n'
                                        f'Ethereum price is {price["ethereum"]["uah"]} UAH\n'
                                        f'Polygon price is {price["matic-network"]["uah"]} UAH\n'
                                        f'Uniswap price is {price["uniswap"]["uah"]} UAH\n', reply_markup=button)
        go_main = bot.send_message(message.chat.id, "Вернуться назад?", reply_markup=button)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == "Главная":
        main(message)




bot.polling()