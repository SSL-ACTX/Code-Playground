import tkinter as tk
from tkinter import scrolledtext
from bardapi import Bard, SESSION_HEADERS
import requests
from datetime import datetime
from IPython.display import clear_output

# Set token
token = 'bard_api.'

# Set session
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", token)

# Create Bard instance
bard = Bard(token=token, session=session, language="en", conversation_id="c_1f04f704a788e6e4", timeout=30)

# Function to save prompt results to a text file
def save_prompt_result(prompt, answer, links):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("prompt_results.txt", "a") as file:
        file.write("Timestamp: " + timestamp + "\n")
        file.write("Prompt: " + prompt + "\n")
        file.write("Answer: " + answer + "\n")
        file.write("Links: " + links + "\n")
        file.write("-" * 50 + "\n")

def reset_application():
    output_text.delete(1.0, tk.END)

def get_answer():
    # Get user input from the entry widget
    prompt = entry.get()
    clear_output(wait=True)
    
    if prompt.lower() == 'exit':
        # Save the prompt result and exit the application
        save_prompt_result(prompt, "", "")
        root.destroy()
    elif prompt.lower() == 'reset':
        # Reset the application
        reset_application()
    else:
        # Get the answer
        answer = bard.get_answer(prompt)['content']
        output_text.insert(tk.END, "User: " + prompt + "\n", "user")  # Add user prompt with 'user' tag
        output_text.insert(tk.END, "Bard: " + answer + "\n", "bot")  # Add bot answer with 'bot' tag

        # Save the prompt result to a text file
        save_prompt_result(prompt, answer, "")

        # Clear the entry widget
        entry.delete(0, tk.END)

def toggle_theme():
    global is_dark_mode
    
    if is_dark_mode:
        # Switch to light mode
        root.config(bg="white")
        entry.config(bg="white", fg="black")
        button.config(bg="white", fg="black")
        output_text.config(bg="white", fg="black")
        toggle_button.config(text="D")
        is_dark_mode = False
    else:
        # Switch to dark mode
        root.config(bg="#212121")
        entry.config(bg="#424242", fg="white")
        button.config(bg="#424242", fg="white")
        output_text.config(bg="#424242", fg="white")
        toggle_button.config(text="L")
        is_dark_mode = True

# Create the Tkinter window
root = tk.Tk()
root.title("Bard GUI (TEST)")

# Default mode is dark mode
is_dark_mode = True

# Create the frame for toggle button
toggle_frame = tk.Frame(root, bg=root.cget("bg"))
toggle_frame.pack(anchor=tk.NE, padx=7, pady=5)

# Create the toggle button to switch between dark mode and light mode
toggle_button = tk.Button(toggle_frame, text="L", command=toggle_theme, bg=root.cget("bg"), fg="black", font=("Arial", 8), bd=0, highlightthickness=0)
toggle_button.pack()

# Create the output text box for prompt results
output_text = scrolledtext.ScrolledText(root, width=65, height=15, bg="#424242", fg="white", font=("Arial", 10))  # Dark mode colors and font
output_text.pack(pady=10)

# Configure tags for user and bot messages
output_text.tag_configure("user", foreground="#ffe5b4")
output_text.tag_configure("bot", foreground="white")

# Create the frame for user input and send button
entry_frame = tk.Frame(root, bg="#424242")
entry_frame.pack(pady=10)

# Create the entry widget for user input
entry = tk.Entry(entry_frame, width=50, bg="#424242", fg="white", font=("Arial", 10))  # Dark mode colors and font
entry.pack(side=tk.LEFT)

# Create the button to get the answer
button = tk.Button(entry_frame, text=">", command=get_answer, bg="#424242", fg="white", font=("Arial", 14))  # Dark mode colors and font
button.pack(side=tk.LEFT, padx=5)

# Bind the Enter key to the Send button
root.bind("<Return>", lambda event: button.invoke())

# Bind the tab key to the toggle theme button
root.bind("<Tab>", lambda event: toggle_button.invoke())

# Bind the escape key to the prompt.lower
root.bind("<Escape>", lambda event: root.destroy())

# Run the Tkinter event loop
root.mainloop()
