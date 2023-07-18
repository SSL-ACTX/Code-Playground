from PIL import Image
import colorama
from colorama import Fore, Style
import os
import time

colorama.init(autoreset=True)

gif_path = "fumo.gif"
frames = []

with Image.open(gif_path) as gif:
    gif.seek(0)
    try:
        while True:
            frame = gif.copy().convert("L")
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

ascii_chars = "@%#*+=-:. "

birthday_text = r"""
                                       ╔♥╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦╦♥╗
                                       ╠♥╣█████████████████████████████████╠♥╣
                                       ╠♥╣█╔╗╔╗█████████╔══╦╗█╔╗╔╗█╔╗██████╠♥╣
                                       ╠♥╣█║╚╝╠═╗╔═╦═╦╦╗║╔╗╠╬╦╣╚╣╚╦╝╠═╗╔╦╗█╠♥╣
                                       ╠♥╣█║╔╗║╬╚╣╬║╬║║║║╔╗║║╔╣╔╣║║╬║╬╚╣║║█╠♥╣
                                       ╠♥╣█╚╝╚╩══╣╔╣╔╬╗║╚══╩╩╝╚═╩╩╩═╩══╬╗║█╠♥╣
                                       ╠♥╣███████╚╝╚╝╚═╝███████████████╚═╝█╠♥╣
                                       ╠♥╣█████████████████████████████████╠♥╣
                                       ╚♥╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩♥╝    
"""
text_color = Fore.CYAN

ascii_width = 100
ascii_height = 50

while True:
    for frame in frames:
        # os.system("cls" if os.name == "nt" else "clear")
        ascii_frame = frame.resize((ascii_width, ascii_height), Image.BILINEAR)
        ascii_frame = ascii_frame.convert("L")
        ascii_text = ""
        
        # Loop :)
        for y in range(ascii_frame.size[1]):
            for x in range(ascii_frame.size[0]):
                pixel = ascii_frame.getpixel((x, y))
                char_index = int(pixel / 255 * (len(ascii_chars) - 1))
                ascii_char = ascii_chars[char_index]
                ascii_text += ascii_char
                
            ascii_text += "\n"
            
        # Print it
        print(Fore.WHITE + Style.BRIGHT + ascii_text)
        print(text_color + Style.BRIGHT + birthday_text)
        
        # Speed
        time.sleep(0.04)
