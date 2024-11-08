from tkinter import *
from tkinter import ttk as t_tk
import Functions as f

def client_interface():

    def get_selected_action(combobox):
        selected_value = combobox.get()
        print("Selected text: ", selected_value)
        root.after(500, get_selected_action, combobox)

        return selected_value

    def get_entry_text():
        # extragem numele topicului si textul la apasarea butonului "Done"
        topicN_extract = topicN_entry.get()
        topicT_extract = topicT_entry.get()

        print("Extracted topic name:", topicN_extract)
        print("Extracted topic text:", topicT_extract)

        topicN_entry.delete(0, END)
        topicT_entry.delete(0, END)

    def task_client(combobox, topicT_entry):
        option = combobox.get()
        if option == "Subscribe":
            topicT_entry.config(state="disabled")
        if option == "Publish":
            topicT_entry.config(state="normal")
        root.after(500, task_client, combobox, topicT_entry)

    # def update_line():
    #     width = root.winfo_width()
    #     height = root.winfo_height()
    #
    #     canvas.delete(ALL)
    #
    #     canvas.create_line(0, 0.23*height, width, 0.23*height, fill="black", width=1.5)
    #
    #     root.after(1, update_line)

    root = Tk()

    root.title("MQTT Client")
    root.geometry("700x600")

    # pentru linia orizontala
    canvas = Canvas(root, width=700, height=600)
    canvas.pack(fill=BOTH, expand=True)
    f.update_line(root, canvas)

    action_label = f.define_label(root, "Action name:", 15, FALSE, 0.05, 0.15, W);
    # action_label = t_tk.Label(root, text="Action name:", font=("Helvetica", 15))
    # action_label.place(relx = 0.05, rely=0.15, anchor=W)

    action_combo = t_tk.Combobox(root,
                                 values=["Publish", "Subscribe"],
                                 font=("Helvetica", 15),
                                 state="readonly"
                                 )
    action_combo.current(0)
    action_combo.place(relx = 0.5, rely = 0.15, anchor=CENTER)


    content_label = f.define_label(root, "Content:", 15, FALSE, 0.05, 0.45, W)
    # content_label=t_tk.Label(root, text="Content: ", font=("Helvetica", 15))
    # content_label.place(relx=0.05, rely=0.45, anchor=W)

    topic_name = f.define_label(root, "Topic name:", 15, FALSE, 0.5, 0.4, CENTER);
    # topic_name = t_tk.Label(root, text="Topic name:", font=("Helvetica", 15))
    # topic_name.place(relx = 0.5, rely=0.4, anchor=CENTER)

    topicN_entry = f.define_entry(root, FALSE, 0.5, 0.45)
    # topicN_entry = t_tk.Entry(root, font=("Arial", 16))
    # topicN_entry.place(relx=0.5, rely=0.45, anchor=CENTER)

    topic_text = f.define_label(root, "Topic text:", 15, FALSE, 0.5, 0.55, CENTER);
    # topic_text = t_tk.Label(root, text="Topic text:", font=("Helvetica", 15))
    # topic_text.place(relx = 0.5, rely=0.55, anchor=CENTER)
    topicT_entry = f.define_entry(root, FALSE, 0.5, 0.60)
    # topicT_entry = t_tk.Entry(root, font=("Arial", 16))
    # topicT_entry.place(relx=0.5, rely=0.60, anchor=CENTER)
    action_combo.bind("<<ComboboxSelected>>", task_client(action_combo, topicT_entry))

    done_btn = Button(root, text="Done", font=('Helvetica', 16, 'bold'), command=get_entry_text)
    done_btn.place(relx=0.9, rely=0.9, anchor=CENTER)

    send_label = f.define_label(root, "Send:", 15, FALSE, 0.5, 0.7, CENTER);
    # send_label = t_tk.Label(root, text="Send:", font=("Helvetica", 15))
    # send_label.place(relx = 0.5, rely=0.70, anchor=CENTER)

    send_combo = t_tk.Combobox(root,
                                 values=["At most once",
                                         "At least once",
                                         "Exactly once"],
                                 font=("Helvetica", 15),
                                 state="readonly")
    send_combo.current(0)
    send_combo.place(relx = 0.5, rely = 0.75, anchor=CENTER)
    send_combo.bind("<<ComboboxSelected>>", get_selected_action(send_combo))

    root.mainloop()

client_interface()