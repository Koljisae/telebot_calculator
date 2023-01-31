import os
import telebot
import re
from dotenv import load_dotenv
from telebot.types import Message
from keyboards import get_calculator_buttons

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))


@bot.message_handler(commands=["start"])
def start_message(message: Message):
    bot.send_message(message.chat.id, "Hello! Write /calculator")


@bot.message_handler(commands=["calculator"])
def calculator(message: Message):
    markup = get_calculator_buttons()
    bot.send_message(message.chat.id, "Welcome to Calculator!", reply_markup=markup)
    bot.register_next_step_handler(message, calculator_editing_message, message_id=None)


def calculator_editing_message(
    message: Message,
    calc_x: str = "",
    calc_operator: str = "",
    calc_y: str = "",
    message_id: int = None
):
    nums_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    operator_list = ["/", "*", "-", "+"]
    current_char = message.text
    bot.delete_message(message.chat.id, message.id)
    if not message_id:
        if current_char in nums_list:
            sent_message = bot.send_message(message.chat.id, current_char)
            bot.register_next_step_handler(
                message,
                calculator_editing_message,
                calc_x=current_char,
                message_id=sent_message.id
            )
        else:
            bot.register_next_step_handler(
                message, calculator_editing_message, message_id
            )
        return
    if current_char == "/exit":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "End calculator.", reply_markup=markup)
        return
    elif re.search(r"[^0-9/*+<=-]+", current_char):
        bot.register_next_step_handler(
            message, calculator_editing_message, message_id=message_id
        )
        return
    elif current_char == "=":
        if calc_x == "0":
            pass
        elif calc_x.split("0") != "":
            calc_x = calc_x.lstrip("0")
        if calc_y.split("0") != '':
            calc_y = calc_y.lstrip("0")
        if calc_x and calc_y and calc_operator:
            calc_x = eval(calc_x + calc_operator + calc_y)
            calc_y, calc_operator = "", ""
            bot.edit_message_text(
                text=str(calc_x) + str(calc_operator) + str(calc_y),
                chat_id=message.chat.id,
                message_id=message_id,
            )
        elif calc_x and calc_operator:
            calc_operator = ""
            bot.edit_message_text(
                text=str(calc_x),
                chat_id=message.chat.id,
                message_id=message_id,
            )
        else:
            pass
        bot.register_next_step_handler(
            message,
            calculator_editing_message,
            str(calc_x),
            calc_operator,
            calc_y,
            message_id
        )
    elif current_char == "<<<":
        if str(calc_x) == "0":
            bot.delete_message(message.chat.id, message_id)
            bot.register_next_step_handler(message, calculator_editing_message, '')
            return
        elif calc_y:
            calc_y = calc_y[:-1]
        elif calc_operator:
            calc_operator = ""
        elif len(calc_x) <= 1:
            calc_x = "0"
        elif calc_x:
            calc_x = calc_x[:-1]
        bot.edit_message_text(
            text=str(calc_x) + str(calc_operator) + str(calc_y),
            chat_id=message.chat.id,
            message_id=message_id,
        )
        bot.register_next_step_handler(
            message,
            calculator_editing_message,
            str(calc_x),
            calc_operator,
            calc_y,
            message_id
        )
    else:
        if calc_operator and calc_y and calc_x and current_char in operator_list:
            calc_x = eval(calc_x + calc_operator + calc_y)
            calc_y, calc_operator = '', current_char
        elif calc_operator == '':
            if current_char in nums_list:
                calc_x += current_char
            elif current_char in operator_list:
                calc_operator += current_char
        elif (
            current_char in operator_list
            and calc_y == ''
            and calc_operator in operator_list
        ):
            calc_operator = current_char
        elif calc_x and calc_operator and current_char in nums_list:
            calc_y += current_char
        bot.edit_message_text(
            text=str(calc_x) + str(calc_operator) + str(calc_y),
            chat_id=message.chat.id,
            message_id=message_id,
        )
        bot.register_next_step_handler(
            message,
            calculator_editing_message,
            str(calc_x),
            calc_operator,
            calc_y,
            message_id
        )


if __name__ == "__main__":
    bot.polling()
