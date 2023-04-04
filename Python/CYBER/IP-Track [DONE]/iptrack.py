import os
import geocoder
import threading
import tkinter as tk
import tkinter.scrolledtext as tkst
from ipwhois import IPWhois
from tkinter import ttk
from tkinter import messagebox
from scapy.all import *

os.system("cls")

packet_count = 0

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#2c3e50")
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tk.Label(self, text="Enter the IP address to monitor:", fg="white", bg="#2c3e50")
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(self, bg="#ffffff", fg="#000000")
        self.ip_entry.pack()
        
        self.start_button = tk.Button(self, text="Scan", command=self.start_sniffing, bg="#ffffff", fg="#000000")
        self.start_button.pack(pady=10)

        self.output_label = tk.Label(self, text="Output:", fg="white", bg="#2c3e50")
        self.output_label.pack()
        self.output_text = tk.Text(self, height=10, bg="#2c3e50", fg="white")
        self.output_text.pack()

    def start_sniffing(self):
        ip_address = self.ip_entry.get()

        if not ip_address:
            messagebox.showerror("Error", "Please enter an IP address.")
            return

        self.output_text.delete(1.0, tk.END)

        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.output_text)

        sniff(filter="tcp", prn=lambda packet: log_tcp(packet, ip_address), timeout=10)

        sys.stdout = old_stdout

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)

def log_tcp(packet, ip_address):
    global packet_count
    if packet.haslayer(TCP):
        if packet[IP].src == ip_address or packet[IP].dst == ip_address:
            if packet_count < 20:
                log_str = "Timestamp: " + str(packet.time) + " | Source IP: " + packet[IP].src + " | Destination IP: " + packet[IP].dst + " | Source Port: " + str(packet[TCP].sport) + " | Destination Port: " + str(packet[TCP].dport) + " | Flags: " + str(packet[TCP].flags)
                print(log_str)
                packet_count += 1

root = tk.Tk()
root.config(bg="#2c3e50")
root.title("Packet Sniffer")
app = App(master=root)


BG_COLOR = "#2c3e50"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#e74c3c"

class IPScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("IP Tracker")
        master.geometry("500x400")
        master.config(bg=BG_COLOR)

        self.ip_input_label = ttk.Label(master, text="Enter IP Address:", foreground=FG_COLOR, background=BG_COLOR, font=("Helvetica", 10))
        self.ip_input_label.pack(pady=5)
        self.ip_input = ttk.Entry(master, font=("Helvetica", 10))
        self.ip_input.pack(pady=5)
        self.scan_button = ttk.Button(master, text="Scan", command=self.scan_ip)
        self.scan_button.pack(pady=5)
        self.output_box = tk.Text(master, font=("Helvetica", 10), wrap="word", state="disabled", height=15, bg=BG_COLOR, fg=FG_COLOR)
        self.output_box.pack(pady=15)
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", foreground=FG_COLOR, background=ACCENT_COLOR, font=("Helvetica", 12))

    def scan_ip(self):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")

        ip_address = self.ip_input.get()

        ip = IPWhois(ip_address)
        result = ip.lookup_rdap()
        output_text = f"IP address: {ip_address}\n"
        output_text += f"Country: {result.get('asn_country_code', 'N/A')}\n"
        output_text += f"Organization: {result.get('asn_description', 'N/A')}\n"
        output_text += f"ISP: {result.get('network', {}).get('name', 'N/A')}\n"
        output_text += f"CIDR: {result.get('network', {}).get('cidr', 'N/A')}\n"

        try:
            output_text += f"NetRange: {result['network']['range']}\n"
        except KeyError:
            output_text += "NetRange: N/A\n"

        try:
            output_text += f"City: {result['city']}\n"
        except KeyError:
            output_text += "City: N/A\n"

        try:
            output_text += f"Region: {result['region']}\n"
        except KeyError:
            output_text += "Region: N/A\n"

        try:
            output_text += f"Postal Code: {result['postal']}\n"
        except KeyError:
            output_text += "Postal Code: N/A\n"
            	
        g = geocoder.ip(ip_address)
        latitude, longitude = g.latlng
        output_text += f"Latitude: {latitude}\n"
        output_text += f"Longitude: {longitude}\n"
        self.output_box.config(state="normal")
        self.output_box.insert("1.0", output_text)
        self.output_box.config(state="disabled")

    def clear_ip_input(self):
        self.ip_input.delete(0, tk.END)

root = tk.Tk()
ip_scanner_gui = IPScannerGUI(root)
app.mainloop()
