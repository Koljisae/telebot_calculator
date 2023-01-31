from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def get_calculator_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    calculator_symbols = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 0,
        "<<<", "=", "+", "-", "*", "/", "/exit"
    ]
    calculator_buttons = []
    for symbol in calculator_symbols:
        calculator_buttons.append(KeyboardButton(str(symbol)))
    markup.add(*calculator_buttons)
    return markup
