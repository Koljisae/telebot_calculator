# telebot_calculator
**telebot_calculator** - tiny [Telegram](https://telegram.org/) bot that can multiply, divide, subtract, sum numbers! Users can interact with bots by sending them commands and messages.
### Telegram token
1. Find [@BotFather](https://t.me/BotFather) in Telegram and write `/start`
2. Write `/token` to get a token **(don't show the token to anyone)**
3. Create a `/newbot`
4. Write a bot nickname.
5. Wtite a username for your bot.
6. DONE!
### How to save a token?
Write your token in file `.env` without quotes.
And this token will be used in `telebot_1.py` file.
```Python
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
```
### Telegram BOT commands
- `/start` - starts bot.
- `/calculator` - starts calculator.
- `/exit` - ends calculator.


