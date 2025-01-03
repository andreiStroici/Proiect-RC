from tkinter import *
import tkinter as t_tk
import time
import psutil
import GPUtil

def define_displayTxt(r, width, height, queue):

    # Create a Text widget
    text_widget = t_tk.Text(r, height=int(0.045*height), width=int(0.063*width))
    text_widget.place(relx=0.00027 * width, rely=0.0001*height)

    # Customize the Text widget appearance
    text_widget.configure(bg="#f0f0f0", fg="#000000", font=('Arial', 12))

    def update_text():
        while not queue.empty():
            destination, message = queue.get()
            if destination != "Interface":
                queue.put((destination, message))
            topic_name = message[0]
            topic_text = message[1]
            text_widget.config(state='normal')
            text_widget.insert(t_tk.END, topic_name + " : " + topic_text + "\n\n")
            text_widget.config(state='disabled')
            text_widget.see(t_tk.END)
        r.after(100, update_text)

    def clear_text():
        """Clear all content in the Text widget."""
        text_widget.config(state='normal')  # Enable editing
        text_widget.delete(1.0, t_tk.END)  # Delete all text
        text_widget.config(state='disabled')  # Disable editing again

    update_text()

    r.after(5000, clear_text)

    return text_widget

def get_measurements(option):
    if option == 'CPU Load':
        # Încărcarea procesorului
        cpu_load = psutil.cpu_percent(interval=1)
        return str(cpu_load)
    elif option == 'Memory Usage':
        # Încărcarea memoriei
        mem_usage = psutil.virtual_memory().percent
        return str(mem_usage)
    elif option == 'GPU Temperature':
        gpus = GPUtil.getGPUs()
        if len(gpus) > 0:
            gpus_temperature = gpus[0].temperature
            return str(gpus_temperature)
        else:
            return "No dedicated GPU found."
    elif option == 'GPU Load':
        gpus = GPUtil.getGPUs()
        if len(gpus) > 0:
            gpus_load = gpus[0].load
            return str(gpus_load)
        else:
            return "No dedicated GPU found."

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