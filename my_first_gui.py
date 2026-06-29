# python -m pip install guizero

# from guizero import App, Text
# app = App(title="Hello world")


# welcome_message = Text(app, text="welcome to my app")
# # All widget code should go here

# app.display()

import tkinter as tk
import os
import sys


def restart_app():
    """
    Restart the current Python script.
    Useful when learning Tkinter and testing changes.
    """
    python = sys.executable
    os.execl(python, python, *sys.argv)


root = tk.Tk()
root.title("My Tkinter Learning App")
root.geometry("400x250")

title_label = tk.Label(
    root,
    text="Hello Rogie!",
    font=("Arial", 18)
)
title_label.pack(pady=20)

message_label = tk.Label(
    root,
    text="Edit the code, save, then click Restart App.",
    font=("Arial", 11)
)
message_label.pack(pady=10)

restart_button = tk.Button(
    root,
    text="Restart App",
    command=restart_app
)
restart_button.pack(pady=20)

root.mainloop()