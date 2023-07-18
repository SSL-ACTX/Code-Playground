# Failed project. Replicate website has a limit of free submitions.

import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from PIL import Image, ImageTk
from datetime import datetime
import random
from fake_useragent import UserAgent


image_src = ""  # Global variable to store the image source URL
driver = None  # Global variable for the WebDriver


def generate_image():
    global image_src, driver  # Declare the variables as global
    if driver is not None:
        driver.quit()  # Quit the previous WebDriver instance, if any

    # Get the user input from the entry widget
    user_input = input_entry.get()

    # Set up Chrome options for running in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--enable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    # Set log level to a lower value (0-3)
    chrome_options.add_argument("--log-level=3")

    # Generate a random MAC address
    mac_address = generate_random_mac_address()

    # Set up the WebDriver (choose the appropriate driver for your browser)
    driver = webdriver.Chrome(options=chrome_options)

    # Set the MAC address and user agent header
    chrome_options.add_argument(f"--user-agent={generate_random_user_agent()}")
    chrome_options.add_argument(f"--use-mock-device-for-media-stream=1")
    chrome_options.add_argument(f"--use-fake-ui-for-media-stream=1")
    chrome_options.add_argument(
        f"--use-file-for-fake-audio-capture=C:/audio.wav")
    chrome_options.add_argument(
        f"--use-file-for-fake-video-capture=C:/video.yuv")
    chrome_options.add_argument(
        f"--use-file-for-fake-video-capture=C:/video.yuv")
    chrome_options.add_argument(
        f"--use-file-for-fake-video-capture=C:/video.yuv")
    chrome_options.add_argument(
        f"--fake-device-id-salt={generate_random_device_id_salt()}")

    # Configure proxy or VPN
    # Uncomment and replace with your proxy or VPN details
    chrome_options.add_argument(f"--proxy-server={'ip'}:{port}")
    # chrome_options.add_argument(f"--proxy-server=socks5://{vpn_server}:{vpn_port}")

    # Navigate to the website
    url = "https://replicate.com/ai-forever/kandinsky-2"
    driver.get(url)

    # Wait for the website to load
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'textarea.form-input.w-full.resize-none'))
    )

    # Find the textarea element
    textarea = driver.find_element(
        By.CSS_SELECTOR, 'textarea.form-input.w-full.resize-none')

    # Clear the default value using JavaScript
    driver.execute_script("arguments[0].value = '';", textarea)

    # Update the value of the textarea with user input
    textarea.send_keys(user_input)

    # Find and click the submit button
    submit_button = driver.find_element(
        By.CSS_SELECTOR, 'button.form-button.mr-2.relative')
    submit_button.click()

    # Wait for the div.mb-lh element to finish loading
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mb-lh'))
    )

    # Wait for the img.lazy element to be visible
    WebDriverWait(driver, timeout=10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'img.lazy'))
    )

    # Find the image element
    image_element = driver.find_element(By.CSS_SELECTOR, 'img.lazy')

    # Get the source URL of the image
    image_src = image_element.get_attribute('src')

    if image_src is not None:
        # Generate a unique filename using the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"output_{timestamp}.png"

        # Download the image with the unique filename
        urllib.request.urlretrieve(image_src, filename)

        # Enable the "View Image" button
        view_button.config(state=tk.NORMAL)

        # Update the preview image
        image = Image.open(filename)
        photo = ImageTk.PhotoImage(image)
        image_preview.config(image=photo)
        image_preview.image = photo
    else:
        messagebox.showerror("Image Generation Failed",
                             "Failed to generate the image.")


def view_image():
    # Open the image using the default image viewer
    image = Image.open("output.png")
    image.show()


def download_image():
    try:
        urllib.request.urlretrieve(image_src, "output.png")
        messagebox.showinfo("Image Downloaded",
                            "Image downloaded successfully!")
    except Exception as e:
        messagebox.showerror(
            "Download Failed", f"Failed to download the image: {str(e)}")


def generate_random_mac_address():
    mac_address = [random.choice('0123456789ABCDEF') for _ in range(12)]
    return ':'.join(mac_address)


def generate_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random


def generate_random_device_id_salt():
    device_id_salt = ''.join(random.choice('0123456789ABCDEF')
                             for _ in range(32))
    return device_id_salt


# Create the Tkinter window
window = tk.Tk()
window.title("Image Generator")
window.geometry("400x450")

# Create the entry widget for user input
input_entry = tk.Entry(window)
input_entry.pack(pady=5)

# Create the Generate Image button
generate_button = tk.Button(
    window, text="Generate Image", command=generate_image)
generate_button.pack(pady=10)

# Create the View Image button (disabled by default)
view_button = tk.Button(
    window, text="View Image", command=view_image, state=tk.DISABLED)
view_button.pack(pady=10)

# Create the Download Image button
download_button = tk.Button(
    window, text="Download Image", command=download_image)
download_button.pack(pady=10)

# Create the image preview
image_preview = tk.Label(window)
image_preview.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
