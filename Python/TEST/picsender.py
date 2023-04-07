import os
import telebot
import tkinter as tk
from tkinter import filedialog, messagebox

bot_token = 'BOT_TOKEN'
chat_id = 'CHAT_ID'
bot = telebot.TeleBot(bot_token, parse_mode=None)

def select_dir():
    """Open a dialog box to select the directory containing the images"""
    dir_path = filedialog.askdirectory()
    if dir_path:
        send_images(dir_path)

def send_images(dir_path):
    """Send all the images in the specified directory to the Telegram bot"""
    img_files = [f for f in os.listdir(dir_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    if not img_files:
        messagebox.showwarning('No images found', 'No images were found in the selected directory.')
        return

    for img_file in img_files:
        with open(os.path.join(dir_path, img_file), 'rb') as img:
            bot.send_photo(chat_id=chat_id, photo=img)

    # Send a message to confirm that all images have been sent
    bot.send_message(chat_id=chat_id, text='All images sent!')

    messagebox.showinfo('Images sent', 'All images were successfully sent to the Telegram bot.')

root = tk.Tk()
root.title('Pic Sender to TG')

select_button = tk.Button(root, text='Select directory', command=select_dir)
select_button.pack(pady=10)

root.mainloop()
