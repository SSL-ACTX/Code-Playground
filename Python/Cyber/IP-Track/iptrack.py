import os
import webbrowser
import geocoder
from ipwhois import IPWhois
import tkinter as tk
from tkinter import ttk

# Color
BG_COLOR = "#2c3e50"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#e74c3c"

class IPScannerGUI:
    def __init__(self, master):
        self.master = master
        master.title("IP Tracker")
        master.geometry("500x400")
        master.config(bg=BG_COLOR)

        # IP Input
        self.ip_input_label = ttk.Label(master, text="Enter IP Address:", foreground=FG_COLOR, background=BG_COLOR, font=("Helvetica", 11))
        self.ip_input_label.pack(pady=10)

        self.ip_input = ttk.Entry(master, font=("Helvetica", 11))
        self.ip_input.pack(pady=10)

        self.scan_button = ttk.Button(master, text="Scan", command=self.scan_ip)
        self.scan_button.pack(pady=10)

        self.output_box = tk.Text(master, font=("Helvetica", 10), wrap="word", state="disabled", height=15, bg=BG_COLOR, fg=FG_COLOR)
        self.output_box.pack(pady=20)

        # Style
        self.style = ttk.Style()
        self.style.configure("Accent.TButton", foreground=FG_COLOR, background=ACCENT_COLOR, font=("Helvetica", 12))

    def scan_ip(self):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")

        ip_address = self.ip_input.get()

        ip = IPWhois(ip_address)
        result = ip.lookup_rdap()

        # Result
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

        # Get the latitude and longitude
        g = geocoder.ip(ip_address)
        latitude, longitude = g.latlng
        output_text += f"Latitude: {latitude}\n"
        output_text += f"Longitude: {longitude}\n"
        
        # Remove comment to automatically open a webbrowser of Google Maps.
        ##map_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
        ##output_text += f"Google Maps URL: {map_url}"

        # Update the output box
        self.output_box.config(state="normal")
        self.output_box.insert("1.0", output_text)
        self.output_box.config(state="disabled")

    def clear_ip_input(self):
        self.ip_input.delete(0, tk.END)

root = tk.Tk()
ip_scanner_gui = IPScannerGUI(root)
root.mainloop()