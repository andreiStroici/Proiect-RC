from tkinter import *
import tkinter as t_tk

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
    canvas.create_line(0, 0.23*height, width, 0.23*height, fill="black", width=1.5)

    r.after(1, update_line, r, canvas)
