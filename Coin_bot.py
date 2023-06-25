import telebot
import requests
from telebot import types
from telebot.types import Message
from config import api_url, group_chat_id, bot, my_user_id

text_list = []

user_data = {}


@bot.message_handler(commands=["start"])
def start_chat(message: Message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = True
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text="Разрешить доступ", url="https://telegram.me/Bit_good_bot?start=auth")
        markup.add(button)
        bot.send_message(message.chat.id, "Для использования всех функций бота, нам потребуется доступ к вашему username. Пожалуйста, разрешите доступ, нажав на кнопку ниже:", reply_markup=markup)
    else:
        text_list.clear()
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = telebot.types.KeyboardButton("Купить криптовалюту")
        item2 = telebot.types.KeyboardButton("Узнать курс криптовалюты")
        item3 = telebot.types.KeyboardButton("/help")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}", reply_markup=markup)
        text_list.append(message.from_user.id)
        text_list.append(message.from_user.username)


@bot.message_handler(commands=["help"])
def show_help(message: Message):
    help_message = "Список доступных команд:\n" \
                   "/start - Начать чат\n" \
                   "/help - Показать список команд\n" \
                   "Узнать курс криптовалюты - Получить информацию о курсе криптовалюты\n" \
                   "Купить криптовалюту - Купить выбранную криптовалюту\n\n" \
                   "Для получения подробной информации, введите команду и следуйте инструкциям."
    bot.reply_to(message, help_message)


@bot.message_handler(func=lambda message: message.text == "Узнать курс криптовалюты")
def handle_crypto(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Crypto Bitcoin (BTC)")
    item2 = telebot.types.KeyboardButton("Crypto Ethereum (ETH)")
    item3 = telebot.types.KeyboardButton("Crypto Stellar (XLM)")
    item4 = telebot.types.KeyboardButton("Crypto Dash (DASH)")
    item5 = telebot.types.KeyboardButton("Crypto Monero (XRM)")
    item6 = telebot.types.KeyboardButton("Crypto Litecoin (LTC)")
    back_button = types.KeyboardButton('Back')
    markup.add(item1, item2, item3, item4, item5, item6, back_button)
    bot.reply_to(message, 'Используйте команду в правильном формате. Например, "Crypto Bitcoin (BTC) или выберите из списка ниже".', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.startswith("Crypto "))
def handle_crypto_command(message):
    # Получение курса криптовалюты
    coin_name = message.text.split(" ")[1].lower()  # Имя криптовалюты, переданное в команде
    response = requests.get(f'{api_url}/simple/price?ids={coin_name}&vs_currencies=usd')
    if response.status_code == 200:
        data = response.json()
        if coin_name in data:
            price = data[coin_name]['usd']
            bot.reply_to(message, f'Текущий курс {coin_name}: ${price}')
        else:
            bot.reply_to(message, 'Криптовалюта не найдена')
    else:
        bot.reply_to(message, 'Ошибка при получении курса криптовалюты')


@bot.message_handler(func=lambda message: message.text.startswith("Crypto"))
def handle_invalid_crypto_command(message):
    bot.reply_to(message, 'Пожалуйста, используйте команду в правильном формате. Например, "Crypto Bitcoin (BTC)".')


@bot.message_handler(func=lambda message: message.text == "Купить криптовалюту")
def buy_crypto(message: Message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Bitcoin")
    item2 = telebot.types.KeyboardButton("Ethereum")
    item3 = telebot.types.KeyboardButton("Litecoin")
    back_button = types.KeyboardButton('Back')
    markup.add(item1, item2, item3, back_button)
    bot.send_message(message.chat.id, f"Выберайте монету", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Back")
def handle_back(message: Message):
    text_list.clear()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Купить криптовалюту")
    item2 = telebot.types.KeyboardButton("Узнать курс криптовалюты")
    item3 = telebot.types.KeyboardButton("/help")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    text_list.append(message.from_user.id)
    text_list.append(message.from_user.username)
    bot.send_message(message.chat.id, "Вы вернулись назад.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ("Bitcoin", "Ethereum", "Litecoin"))
def handle_message(message: Message):
    coin_name = message.text.lower()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("1.0")
    item2 = telebot.types.KeyboardButton("2.0")
    item3 = telebot.types.KeyboardButton("3.0")
    back_button = types.KeyboardButton('Back')
    markup.add(item1, item2, item3, back_button)
    text_list.append(message.text)
    bot.send_message(message.chat.id, "Выберите количество но дробное. Пример 1.3543", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_submit(message: Message):
    mess = message.text
    if len(text_list) < 3:
        bot.send_message(message.chat.id, "Неверная команда. Напишите /start, чтобы начать.")
    else:
        coin = text_list[2].lower()

    def calculate_coin_value(coin_id, amount):
        url = f'{api_url}/simple/price?ids={coin_id}&vs_currencies=usd'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                price = data[coin_id]['usd']
                price_float = float(price)
                amount_float = float(amount)
                value = price_float * amount_float
                rounded_value = round(value, 2)
                percentage = (1 / 100) * value
                rounded_percentage = round(percentage, 2)
                total_amount = rounded_value + rounded_percentage

                bot.send_message(message.chat.id,
                                 f"Сумма для оплаты перевода: {rounded_value} + 1% процент от суммы перевода {rounded_percentage}\nОбщая сумма к оплате {total_amount}$")
                bot.send_message(message.chat.id,
                                 "После отправки заявки в течение 30 минут с вами свяжется наш оператор и после оплаты сделает перевод по данным реквизитам, которые вы ему отправите. Спасибо вам!\n"
                                 "если будут вопросы можете написать нашему оператору лично @GeramSup")
            else:
                bot.send_message(message.chat.id, 'Криптовалюта не найдена')
        else:
            bot.send_message(message.chat.id, 'Ошибка при получении курса криптовалюты')

    if len(text_list) == 4:
        if mess.lower() == "отправить заявку":
            send_request_to_group()
            back_button = types.KeyboardButton('Back')
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(back_button)
            bot.reply_to(message, f"Ваша заявка отправлена. Ожидайте, с вами свяжется наш оператор.", reply_markup=markup)
    else:
        if len(text_list) == 3:
            try:
                number = float(message.text)
                text_list.append(number)
                send_confirmation_message(message)
                calculate_coin_value(coin, text_list[3])
            except ValueError:
                bot.reply_to(message, f"Неправильный формат. Пример 1.234")


def send_confirmation_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Отправить заявку")
    back_button = types.KeyboardButton('Back')
    markup.add(item1, back_button)
    bot.reply_to(message, f"Вы ввели количество: {text_list[3]}")
    bot.send_message(message.chat.id,
                     f"Ваша заявка {text_list[0]}:\n Имя пользователя: {text_list[1]}\n Криптовалюта: {text_list[2]}\n Количество: {text_list[3]}\n Если данные верны, пожалуйста, подтвердите",
                     reply_markup=markup)


def send_request_to_group():
    bot.send_message(group_chat_id,
                     f"Новая заявка от пользователя {text_list[0]}:\n Имя пользователя: {text_list[1]}\n Криптовалюта: {text_list[2]}\n Количество: {text_list[3]}")


bot.polling(none_stop=True)




