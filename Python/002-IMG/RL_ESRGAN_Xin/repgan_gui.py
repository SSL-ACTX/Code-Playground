import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import replicate

class RealESRGANUpscaler:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-ESRGAN Upscaler")
        self.root.configure(bg="#232323")
        self.root.geometry("400x260")

        self.scale_label = tk.Label(self.root, text="Select Scale:", bg="#232323", fg="white")
        self.scale_label.pack(padx=10, pady=10)
        self.scale_var = tk.StringVar(value="4")
        self.scale_menu = tk.OptionMenu(self.root, self.scale_var, "2", "3", "4", "5", "6", "7", "8")
        self.scale_menu.config(bg="#4f4f4f", fg="white", activebackground="#4f4f4f", activeforeground="white")
        self.scale_menu.pack(padx=10, pady=5)

        self.version_label = tk.Label(self.root, text="Select Version:", bg="#232323", fg="white")
        self.version_label.pack(padx=10, pady=10)
        self.version_var = tk.StringVar(value="Anime - anime6B")
        self.version_menu = tk.OptionMenu(self.root, self.version_var, "General - RealESRGANplus", "General - v3", "Anime - anime6B", "AnimeVideo - v3")
        self.version_menu.config(bg="#4f4f4f", fg="white", activebackground="#4f4f4f", activeforeground="white")
        self.version_menu.pack(padx=10, pady=5)

        self.upscale_button = tk.Button(self.root, text="Upscale Image", bg="#4f4f4f", fg="white", command=self.upscale_image)
        self.upscale_button.pack(padx=10, pady=20)

    def run(self):
        self.root.mainloop()

    def upscale_image(self):
        input_path = filedialog.askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if not input_path:
            return

        client = replicate.Client(api_token='replicate_api_token')
        options = {}
        output = client.run(
            "xinntao/realesrgan:1b976a4d456ed9e4d1a846597b7614e79eadad3032e9124fa63859db0fd59b56",
            input={"img": open(input_path, "rb"), "scale": int(self.scale_var.get()), "version": self.version_var.get(), "tile": 0},
            options=options
        )
        url = output
        response = requests.get(url)

        output_path = filedialog.asksaveasfilename(title="Save Output Image", defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if output_path:
            with open(output_path, "wb") as f:
                f.write(response.content)
            messagebox.showinfo(title="Success", message="Image upscaled and saved successfully!")
        else:
            messagebox.showerror(title="Error", message="Output file path not selected!")

app = RealESRGANUpscaler()
app.run()
