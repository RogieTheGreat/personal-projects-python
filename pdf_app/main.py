import tkinter as tk
from tkinter import filedialog, messagebox
from converter import convert_image

selected_file = ""


def browse_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp")
        ]
    )

    if selected_file:
        file_label.config(text=selected_file)


def convert():
    if not selected_file:
        messagebox.showerror("Error", "Please select a file.")
        return

    output_format = format_var.get().lower()

    save_file = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=f".{output_format}",
        filetypes=[
            (output_format.upper(), f"*.{output_format}")
        ]
    )

    if not save_file:
        return

    try:
        convert_image(selected_file, save_file)

        messagebox.showinfo(
            "Success",
            f"File saved successfully:\n\n{save_file}"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


root = tk.Tk()
root.title("TINKR Converter")
root.geometry("500x300")

title = tk.Label(
    root,
    text="TINKR CONVERTER",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

browse_btn = tk.Button(
    root,
    text="Select Image",
    command=browse_file,
    width=20
)
browse_btn.pack()

file_label = tk.Label(
    root,
    text="No file selected",
    wraplength=450
)
file_label.pack(pady=10)

format_var = tk.StringVar()
format_var.set("PDF")

formats = tk.OptionMenu(
    root,
    format_var,
    "PDF",
    "PNG",
    "JPG"
)
formats.pack(pady=10)

convert_btn = tk.Button(
    root,
    text="Convert",
    command=convert,
    width=20
)
convert_btn.pack(pady=20)

root.mainloop()