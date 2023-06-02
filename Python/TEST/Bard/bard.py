from bardapi import Bard, SESSION_HEADERS
import requests
import telebot
import time
import os
import sys
import json

bot = telebot.TeleBot("BOT_TOKEN")

token = 'BARD_TOKEN'

MAX_RETRIES = 3
RETRY_DELAY = 3

CONFIG_FOLDER = "user_data"

# Create the user data folder if it doesn't exist
if not os.path.exists(CONFIG_FOLDER):
    os.makedirs(CONFIG_FOLDER)

# Get the filename for the user's configuration


def get_user_config_filename(chat_id):
    return f"{CONFIG_FOLDER}/{chat_id}_config.json"

# Load user configurations from the file


def load_user_config(chat_id):
    filename = get_user_config_filename(chat_id)
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user configurations to the file


def save_user_config(chat_id, user_data):
    filename = get_user_config_filename(chat_id)
    with open(filename, "w") as file:
        json.dump(user_data, file)

# Initialize user data from the file


def initialize_user_data(chat_id):
    user_data = load_user_config(chat_id)
    if not user_data:
        user_data = {}
        save_user_config(chat_id, user_data)
    return user_data


session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", token)


def ask_for_language(message):
    chat_id = message.chat.id
    language_options = [["chinese (simplified)", "english"], [
        "arabic", "japanese"]]
    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(version_option)
                 for version_option in language_options[0]])
    keyboard.add(*[telebot.types.KeyboardButton(version_option)
                 for version_option in language_options[1]])
    bot.send_message(
        chat_id, "What language do you want to use? (You can also input your preferred language.)\n Note. Use small letters.", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_language)


def get_language(message):
    chat_id = message.chat.id
    language = message.text.lower()  # Convert language input to lowercase
    # Save the user's selected language
    user_data = initialize_user_data(chat_id)
    user_data["language"] = language
    save_user_config(chat_id, user_data)  # Update the JSON file


@bot.message_handler(commands=['language'])
def language_command(message):
    chat_id = message.chat.id
    user_data = initialize_user_data(chat_id)
    if "language" not in user_data:
        ask_for_language(message)
    else:
        bot.send_message(
            chat_id, "You have already selected a language. If you want to change it, please /reset the bot.")


@bot.message_handler(commands=['help'])
def reset_command(message):
    chat_id = message.chat.id
    # Send the help message
    help_message = "Here are some available commands:\n\n" \
        "/help: This help message.\n"\
        "/language: Change current language. (Default: English)\n"\
        "/reset: Reset chat and language.\n\n"\
        " Latest added features:\n"\
        "      - Images (Testing)\n"\
        "      - Links (Testing)\n"\
        "      - Language Support (40+ Languages)\n"\
        "      - Chat Continuation (Testing)\n"
    bot.send_message(chat_id, help_message)


@bot.message_handler(commands=['reset'])
def reset_command(message):
    chat_id = message.chat.id
    filename = get_user_config_filename(chat_id)
    if os.path.exists(filename):
        os.remove(filename)
        bot.send_message(
            chat_id, "Language reset. Please select a new language using the /language command.")
    else:
        bot.send_message(chat_id, "You haven't selected a language yet.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_input = message.text
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)  # Optional delay to simulate typing
    user_data = initialize_user_data(chat_id)
    language = user_data.get("language")
    if language:
        bard = Bard(token=token, session=session, timeout=40,
                    language=language)  # Initialize Bard instance
        res = bard.get_answer(user_input)
        answer = res['content']
        if res['images']:
            for image in res['images']:
                bot.send_photo(chat_id, image)
        bot.send_message(chat_id, answer)
    else:
        bot.send_message(
            chat_id, "Please select a language using the /language command.")


while True:
    try:
        bot.polling()

    except Exception as e:
        print(f"An error occurred: {e}")
        retries = 0
        while retries < MAX_RETRIES:
            print(f"Retrying ({retries+1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
            retries += 1
        else:
            print("Maximum retries reached. Restarting the program...")
            python = sys.executable
            os.execl(python, python, *sys.argv)
