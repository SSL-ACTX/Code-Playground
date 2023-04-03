from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance
import os
import tkinter as tk
from tkinter import filedialog

# Set dark theme
root = tk.Tk()
root.title("Image Upscaler")
root.config(bg="#121212")
root.option_add("*foreground", "white")
root.option_add("*background", "#121212")

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(0, file_path)

def upscale_image():
    input_path = Path(input_path_entry.get())
    if not input_path.exists():
        tk.messagebox.showerror("Error", "Input image does not exist.")
        return

    # Open the original image
    with Image.open(input_path) as image:
        # Apply a denoising filter
        denoised_image = image.filter(ImageFilter.GaussianBlur(radius=0.7))

        # Get user input for the upscaling level
        upscale_factor = int(upscale_factor_entry.get())

        # Upscale the image using Lanczos filter
        upscaled_image = denoised_image.resize((image.width * upscale_factor, image.height * upscale_factor), resample=Image.LANCZOS)

        # Apply a sharpen filter to improve image quality
        sharpened_image = upscaled_image.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=3))

        # Apply color correction
        enhancer = ImageEnhance.Color(sharpened_image)
        colorful_image = enhancer.enhance(1.2)  # Increase color saturation by 20%
        enhancer = ImageEnhance.Brightness(colorful_image)
        brightened_image = enhancer.enhance(1.1)  # Increase brightness by 10%

    # Save the improved image
    improved_image_path = Path("improved_image.jpg")
    brightened_image.save(improved_image_path)

    tk.messagebox.showinfo("Success", f"Saved improved image to {improved_image_path}")

input_path_label = tk.Label(root, text="Input image path:", bg="#121212", fg="white")
input_path_label.grid(row=0, column=0, pady=5)

input_path_entry = tk.Entry(root, bg="#242424", fg="white")
input_path_entry.grid(row=0, column=1)

input_path_button = tk.Button(root, text="Open", command=open_file, bg="#2f2f2f", fg="white", activebackground="#1f1f1f", activeforeground="white", bd=0, padx=10)
input_path_button.grid(row=0, column=2, pady=5)

upscale_factor_label = tk.Label(root, text="Upscale factor:", bg="#121212", fg="white", padx=10)
upscale_factor_label.grid(row=1, column=0, pady=5)

upscale_factor_entry = tk.Entry(root, bg="#242424", fg="white")
upscale_factor_entry.grid(row=1, column=1)

upscale_button = tk.Button(root, text="Upscale", command=upscale_image, bg="#2f2f2f", fg="white", activebackground="#1f1f1f", activeforeground="white", bd=0, padx=10)
upscale_button.grid(row=2, column=1, pady=5)

root.mainloop()
