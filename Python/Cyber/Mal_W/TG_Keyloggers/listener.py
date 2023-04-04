import socket
import telebot

# TG
TOKEN = 'token'
CHAT_ID = 'chat_id'

bot = telebot.TeleBot(token=TOKEN)
sock = socket.socket()

# IP & Port
host = '192.168.0.125'
port = 5555

sock.bind((host, port))
sock.listen(5)

print("Python server listening for incoming Android data...")

while True:
    # Connection
    conn, addr = sock.accept()

    print("Android app connected: ", addr)
    # Receiver
    data = conn.recv(1024).decode('utf-8')
    print("Data received from Android app: ", data)
    # TG Send
    bot.send_message(chat_id=CHAT_ID, text=data)

    conn.close()
