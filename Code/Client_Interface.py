from tkinter import *
from tkinter import ttk as t_tk

def get_entry_text():
    # extragem numele topicului si textul la apasarea butonului "Done"
    topicN_extract = topicN_entry.get()
    topicT_extract = topicT_entry.get()

    print("Extracted topic name:", topicN_extract)
    print("Extracted topic text:", topicT_extract)

    topicN_entry.delete(0, END)
    topicT_entry.delete(0, END)


def update_line():
    width = root.winfo_width()
    height = root.winfo_height()

    canvas.delete(ALL)

    canvas.create_line(0, 0.23*height, width, 0.23*height, fill="black", width=1.5)

    root.after(1, update_line)

root = Tk()

root.title("MQTT Client")
root.geometry("700x600")

canvas = Canvas(root, width=700, height=600)
canvas.pack(fill=BOTH, expand=True)


action_label = t_tk.Label(root, text="Action name:", font=("Helvetica", 15))
action_label.place(relx = 0.05, rely=0.15, anchor=W)

action_combo = t_tk.Combobox(root,
                             values=["Publish", "Subscribe"],
                             font=("Helvetica", 15),
                             state="readonly")
action_combo.current(0)
action_combo.place(relx = 0.5, rely = 0.15, anchor=CENTER)

update_line()

content_label=t_tk.Label(root, text="Content: ", font=("Helvetica", 15))
content_label.place(relx=0.05, rely=0.45, anchor=W)

topic_name = t_tk.Label(root, text="Topic name:", font=("Helvetica", 15))
topic_name.place(relx = 0.5, rely=0.4, anchor=CENTER)
topicN_entry = t_tk.Entry(root, font=("Arial", 16))
topicN_entry.place(relx=0.5, rely=0.45, anchor=CENTER)

topic_text = t_tk.Label(root, text="Topic text:", font=("Helvetica", 15))
topic_text.place(relx = 0.5, rely=0.55, anchor=CENTER)
topicT_entry = t_tk.Entry(root, font=("Arial", 16))
topicT_entry.place(relx=0.5, rely=0.60, anchor=CENTER)

login_btn = Button(root, text="Done", font=('Helvetica', 16, 'bold'), command=get_entry_text)
login_btn.place(relx=0.9, rely=0.9, anchor=CENTER)

root.mainloop()