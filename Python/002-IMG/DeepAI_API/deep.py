import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import shutil
import os

# Dark mode theme colors
DARK_BG = "#282828"
DARK_FG = "#FFFFFF"
DARK_BUTTON_BG = "#383838"
DARK_BUTTON_FG = "#FFFFFF"

class App:
    def __init__(self, master):
        self.master = master
        master.title("Deep Upscaler")
        master.configure(bg=DARK_BG)

        # Labels
        self.image_label = tk.Label(master, text="No image selected", bg=DARK_BG, fg=DARK_FG)
        self.image_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Buttons
        self.select_button = tk.Button(master, text="Select Image", command=self.select_image, bg=DARK_BUTTON_BG, fg=DARK_BUTTON_FG)
        self.select_button.grid(row=1, column=0, padx=10, pady=10)

        self.upscale_button = tk.Button(master, text="Upscale Image", command=self.upscale_image, bg=DARK_BUTTON_BG, fg=DARK_BUTTON_FG)
        self.upscale_button.grid(row=1, column=1, padx=10, pady=10)

        self.quit_button = tk.Button(master, text="Quit", command=self.quit, bg=DARK_BUTTON_BG, fg=DARK_BUTTON_FG)
        self.quit_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    def select_image(self):
        filetypes = (
            ('JPEG files', '*.jpg'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        )
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )
        self.image_label.config(text=filepath)

    def upscale_image(self):
        image_path = self.image_label.cget('text')

        if not image_path:
            messagebox.showerror("Error", "No image selected.")
            return

        try:
            r = requests.post(
                "https://api.deepai.org/api/torch-srgan",
                files={
                    'image': open(image_path, 'rb'),
                },
                headers={'api-key': 'YOUR-API-KEY'}
            )
            response_data = r.json()
            output_url = response_data['output_url']

            # Download the upscaled image
            response = requests.get(output_url, stream=True)
            with open('upscaled_image.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            del response

            messagebox.showinfo("Success", "Image upscaled and saved as 'upscaled_image.jpg'.")
        except:
            messagebox.showerror("Error", "An error occurred during the upscaling process.")

    def quit(self):
        self.master.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
