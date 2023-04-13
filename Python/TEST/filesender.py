import os
import telebot
import tkinter as tk
from tkinter import filedialog, messagebox

bot_token = 'bot_token'
chat_id = 'chat_id'
bot = telebot.TeleBot(bot_token, parse_mode=None)

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        send_file(file_path)

def send_file(file_path):
    with open(file_path, 'rb') as f:
        bot.send_document(chat_id=chat_id, document=f, caption=os.path.basename(file_path))

    bot.send_message(chat_id=chat_id, text='File sent!')

    messagebox.showinfo('File sent', 'The file was successfully sent to the Telegram bot.')

root = tk.Tk()
root.title('Send file to Telegram bot')

select_button = tk.Button(root, text='Select file', command=select_file)
select_button.pack(pady=10)

root.mainloop()
