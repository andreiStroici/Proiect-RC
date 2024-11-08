from tkinter import *
from tkinter import ttk as t_tk

def get_entry_text():
    # extragem username-ul și parola la apăsarea butonului "Login"
    name_extract = name_entry.get()
    pass_extract = pass_entry.get()

    print("Extracted name:", name_extract)
    print("Extracted password:", pass_extract)


root = Tk()
root.title("MQTT Client")
root.geometry("600x500")

title_label = t_tk.Label(root, text="Client Connect Interface", font=("Helvetica", 18, "bold"))
title_label.place(relx=0.5, rely=0.10, anchor=CENTER)

name_label = t_tk.Label(root, text="Username", font=("Helvetica", 16))
name_entry = t_tk.Entry(root, font=("Arial", 16))
name_label.place(relx=0.5, rely=0.25, anchor=CENTER)
name_entry.place(relx=0.5, rely=0.30, anchor=CENTER)

pass_label = t_tk.Label(root, text="Password", font=("Helvetica", 16))
pass_entry = t_tk.Entry(root, font=("Arial", 16), show="*")
pass_label.place(relx=0.5, rely=0.45, anchor=CENTER)
pass_entry.place(relx=0.5, rely=0.50, anchor=CENTER)



login_btn = Button(root, text="Login", font=('Helvetica', 16, 'bold'), command=get_entry_text)
login_btn.place(relx=0.5, rely=0.65, anchor=CENTER)



root.mainloop()