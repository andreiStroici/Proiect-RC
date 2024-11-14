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

    root = Tk()

    root.title("MQTT Client")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{int(width)}x{int(height)}")

    # pentru linia orizontala
    canvas = Canvas(root, width=width, height=height)
    canvas.pack(fill=BOTH, expand=True)
    f.update_line(root, canvas)

    f.define_label(root, "Action name:", 15, FALSE, 0.02, 0.15, W)

    action_combo = t_tk.Combobox(root,
                                 values=["Publish", "Subscribe"],
                                 font=("Helvetica", 15),
                                 state="readonly"
                                 )
    action_combo.current(0)
    action_combo.place(relx=0.23, rely=0.20, anchor=CENTER)

    f.define_label(root, "Content:", 15, FALSE, 0.02, 0.45, W)

    f.define_label(root, "Topic name:", 15, FALSE, 0.2, 0.5, CENTER)
    topicN_entry = f.define_entry(root, FALSE, 0.2, 0.55)

    f.define_label(root, "Topic text:", 15, FALSE, 0.2, 0.60, CENTER)
    topicT_entry = f.define_entry(root, FALSE, 0.2, 0.65)

    action_combo.bind("<<ComboboxSelected>>", task_client(action_combo, topicT_entry))

    done_btn = Button(root, text="Done", font=('Helvetica', 16, 'bold'), command=get_entry_text)
    done_btn.place(relx=0.2, rely=0.85, anchor=CENTER)

    f.define_label(root, "Send:", 15, FALSE, 0.2, 0.7, CENTER)

    send_combo = t_tk.Combobox(root,
                               values=["At most once",
                                       "At least once",
                                       "Exactly once"],
                               font=("Helvetica", 15),
                               state="readonly")
    send_combo.current(0)
    send_combo.place(relx=0.2, rely=0.75, anchor=CENTER)
    send_combo.bind("<<ComboboxSelected>>", get_selected_action(send_combo))

    text_var = StringVar()
    f.define_label(root, "Subscriptions", 25, FALSE, 0.72, 0.05, CENTER)
    f.define_displayTxt(root, width, height)

    # f.update_text(root, text_var)

    root.mainloop()


client_interface()
