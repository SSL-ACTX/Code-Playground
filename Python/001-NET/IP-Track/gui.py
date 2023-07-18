import os
import webbrowser
import geocoder
from ipwhois import IPWhois
import io
import urllib.request
from PIL import Image, ImageTk
import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("IP Scanner")

# Create a frame for the sidebar and map image
sidebar = tk.Frame(root, width=250, bg='gray', height=500, padx=10, pady=10)
sidebar.pack(side='left', fill='y')

# Create a label for the map image
map_label = tk.Label(sidebar)
map_label.pack()

# Create a frame for the IP details
details_frame = tk.Frame(root, padx=10, pady=10)
details_frame.pack(side='right')

# Create a label for the IP address input
ip_label = tk.Label(details_frame, text="Enter the IP address to scan:")
ip_label.pack()

# Create an entry box for the IP address
ip_entry = tk.Entry(details_frame, width=30)
ip_entry.pack()

def scan_ip():
    # Clear any existing map image
    map_label.config(image='')

    # Get the IP address from the entry box
    ip_address = ip_entry.get()

    # Perform the IP lookup
    ip = IPWhois(ip_address)
    result = ip.lookup_rdap()

    # Print the details of the IP address
    ip_details = f"IP address: {ip_address}\nCountry: {result['asn_country_code']}\nOrganization: {result['asn_description']}\nISP: {result['network']['name']}\nCIDR: {result['network']['cidr']}"

    try:
        ip_details += f"\nNetRange: {result['network']['range']}"
    except KeyError:
        ip_details += "\nNetRange: N/A"

    try:
        ip_details += f"\nCity: {result['city']}"
    except KeyError:
        ip_details += "\nCity: N/A"

    try:
        ip_details += f"\nRegion: {result['region']}"
    except KeyError:
        ip_details += "\nRegion: N/A"

    try:
        ip_details += f"\nPostal Code: {result['postal']}"
    except KeyError:
        ip_details += "\nPostal Code: N/A"

    # Get the latitude and longitude coordinates of the IP address using the geocoder library
    g = geocoder.ip(ip_address)
    latitude, longitude = g.latlng

    # Update the map image
    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=12&size=500x500&markers=color:red%7Clabel:%7C{latitude},{longitude}&key=YOUR_API_KEY_HERE"
    map_request = urllib.request.urlopen(map_url)
    map_image = Image.open(io.BytesIO(map_request.read()))
    map_image = ImageTk.PhotoImage(map_image)
    map_label.config(image=map_image)
    map_label.image = map_image

    # Update the details label
    details_label.config(text=ip_details)

    # Open Google Maps in a web browser with the location displayed
    map_url = "https://www.google.com/maps/search/?api=1&query=" + str(latitude) + "," + str(longitude)
    webbrowser.open_new_tab(map_url)

# Create a button to scan the IP address
scan_button = tk.Button(details_frame, text="Scan", command=scan_ip)
scan_button.pack()

# Create a label for the IP details
details_label = tk.Label(details_frame, text="")
details_label.pack()

clear_button = tk.Button(details_frame, text="Clear", command=lambda: (ip_entry.delete(0, 'end'), details_label.config(text=""), map_label.config(image='')))
clear_button.pack()
root.mainloop()