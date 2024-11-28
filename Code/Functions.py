from tkinter import *
import tkinter as t_tk
import time

def define_displayTxt(r, width, height):

    # Create a Text widget
    text_widget = t_tk.Text(r, height=int(0.045*height), width=int(0.063*width))
    text_widget.place(relx=0.00027 * width, rely=0.0001*height)

    # Customize the Text widget appearance
    text_widget.configure(bg="#f0f0f0", fg="#000000", font=('Arial', 12))

    # Add some sample text
    # text_widget.insert(t_tk.END, text_var.get()) ????
    text_widget.config(state='disabled')

    return text_widget

def define_label(r, text, size, boldON, x, y, anchor):
    if boldON == TRUE:
        label = t_tk.Label(r, text=text, font=("Helvetica", size, "bold"))
    else:
        label = t_tk.Label(r, text=text, font=("Helvetica", size))
    label.place(relx=x, rely=y, anchor=anchor)
    return label


def define_entry(r, showON, x, y):
    if showON == TRUE:
        entry = t_tk.Entry(r, font=("Arial", 16), show="*")
    else:
        entry = t_tk.Entry(r, font=("Arial", 16))
    entry.place(relx=x, rely=y, anchor=CENTER)
    return entry


def update_line(r, canvas):
    width = r.winfo_width()
    height = r.winfo_height()

    canvas.delete(ALL)
    canvas.create_line(0, 0.23 * height, 0.4 * width, 0.23 * height, fill="black", width=1.5)
    canvas.create_line(0.4 * width, 0, 0.4 * width, height, fill="black", width=1.5)
    canvas.place(relx=0, rely=0)

    r.after(1, update_line, r, canvas)