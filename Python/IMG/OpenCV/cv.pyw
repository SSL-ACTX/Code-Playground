import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

os.system("cls")

# Define the dark theme colors
dark_bg = '#212121'
dark_fg = 'white'
dark_btn_bg = '#424242'
dark_btn_fg = 'white'

# Create a function to upscale and enhance the image
def enhance_image():
    # Get the filename of the image to be processed
    file_path = filedialog.askopenfilename(title='Image', filetypes=[('Image Files', '*.jpg;*.jpeg;*.png')])
    if not file_path:
        return

    # Load the image
    img = cv2.imread(file_path)

    # Upscale the image
    upscaled_img = cv2.resize(img, None, fx=int(upscale_var.get()), fy=int(upscale_var.get()), interpolation=cv2.INTER_CUBIC)

    # Get the value of the sharpening slider
    sharpen_factor = sharpen_slider.get()

    # Create a Gaussian kernel with the specified standard deviation
    kernel_size = int(3 + sharpen_factor * 2)
    kernel = cv2.getGaussianKernel(kernel_size, sharpen_factor)

    # Apply denoising filter
    denoise_type = denoise_var.get()
    if denoise_type == 'Gaussian':
        denoised_img = cv2.GaussianBlur(upscaled_img, (int(kernel_var.get()), int(kernel_var.get())), 0)
    elif denoise_type == 'Median':
        denoised_img = cv2.medianBlur(upscaled_img, int(kernel_var.get()))
    elif denoise_type == 'Bilateral':
        # Get the kernel size and sigma values
        kernel_size = int(denoise_kernel_var.get())
        sigma = int(denoise_sigma_var.get())

        # Apply the bilateral filter
        denoised_img = cv2.bilateralFilter(img, kernel_size, sigma, sigma)

    else:
        denoised_img = upscaled_img

    # Apply the kernel to the denoised image
    enhanced_img = cv2.filter2D(denoised_img, -1, kernel)

    # Save the upscaled image
    cv2.imwrite('upscaled_image.jpg', upscaled_img)

    # Display the original image and enhanced image
    #cv2.imshow('Original Image', img)
    #cv2.imshow('Enhanced Image', enhanced_img)


# Create the main window
root = tk.Tk()
root.title('OpenCV Upscaler')
root.configure(bg=dark_bg)

# Create a frame to hold the options
options_frame = tk.Frame(root, bg=dark_bg)
options_frame.pack(padx=10, pady=10)

# Create the upscaling size option
upscale_label = tk.Label(options_frame, text='Upscaling Size:', fg=dark_fg, bg=dark_bg)
upscale_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

upscale_var = tk.StringVar()
upscale_var.set('2')

upscale_entry = tk.Entry(options_frame, textvariable=upscale_var, bg=dark_btn_bg, fg=dark_btn_fg)
upscale_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Create the sharpening filter option
sharpen_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, label="Sharpening Factor", bg=dark_bg, fg=dark_fg, troughcolor=dark_btn_bg, highlightthickness=0)
sharpen_slider.pack(padx=10, pady=10)

# Create the denoising filter option
denoise_label = tk.Label(options_frame, text='Denoising Filter:', fg=dark_fg, bg=dark_bg)
denoise_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

denoise_var = tk.StringVar()
denoise_var.set('None')

denoise_dropdown = ttk.Combobox(options_frame, textvariable=denoise_var, values=['None', 'Gaussian', 'Median', 'Bilateral'], state='readonly', background=dark_btn_bg, foreground=dark_btn_fg)
denoise_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='w')

denoise_label = tk.Label(options_frame, text='Denoising Kernel:', fg=dark_fg, bg=dark_bg)
denoise_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

denoise_kernel_var = tk.StringVar()
denoise_kernel_var.set('3')

denoise_kernel_entry = tk.Entry(options_frame, textvariable=denoise_kernel_var, bg=dark_btn_bg, fg=dark_btn_fg)
denoise_kernel_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

denoise_sigma_var = tk.StringVar()
denoise_sigma_var.set('1')

denoise_sigma_label = tk.Label(options_frame, text='Denoising Sigma:', fg=dark_fg, bg=dark_bg)
denoise_sigma_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')

denoise_sigma_entry = tk.Entry(options_frame, textvariable=denoise_sigma_var, bg=dark_btn_bg, fg=dark_btn_fg)
denoise_sigma_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

button = tk.Button(root, text='Enhance Image', command=enhance_image, bg=dark_btn_bg, fg=dark_btn_fg)
button.pack(padx=10, pady=10)

# Run the main event loop
root.mainloop()

