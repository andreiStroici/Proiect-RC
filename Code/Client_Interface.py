import tkinter
from tkinter import *
from tkinter import ttk as t_tk
import Functions as f
from Code.Functions import get_measurements


class Client_Interface():
    def __init__(self, queue):
        self.queue = queue
        self.root = Tk()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.title("MQTT Client")
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{int(width)}x{int(height)}")

        # desenarea liniilor
        canvas = Canvas(self.root, width=width, height=height)
        canvas.pack(fill=BOTH, expand=True)
        f.update_line(self.root, canvas)

        f.define_label(self.root, "Action name:", 15, FALSE, 0.02, 0.15, W)

        action_combo = t_tk.Combobox(self.root,
                                     values=["Publish", "Subscribe", "Unsubscribe"],
                                     font=("Helvetica", 15),
                                     state="readonly")
        action_combo.current(0)
        action_combo.place(relx=0.23, rely=0.20, anchor=CENTER)

        f.define_label(self.root, "Content:", 15, FALSE, 0.02, 0.45, W)

        f.define_label(self.root, "Topic name:", 15, FALSE, 0.2, 0.5, CENTER)
        # self.topicN_entry = f.define_entry(self.root, FALSE, 0.2, 0.55)
        self.topicN_option = t_tk.Combobox(self.root, values=['CPU Temperature', 'CPU Load', 'Memory Usage'],
                                           font=("Helvetica", 15),
                                           state='readonly')
        self.topicN_option.current(0)
        self.topicN_option.place(relx=0.2, rely=0.55, anchor=CENTER)

        f.define_label(self.root, "Topic text:", 15, FALSE, 0.2, 0.60, CENTER)
        self.topicT_entry = f.define_entry(self.root, FALSE, 0.2, 0.65)

        action_combo.bind("<<ComboboxSelected>>", self.task_client(action_combo, self.topicT_entry))

        f.define_label(self.root, "Send:", 15, FALSE, 0.2, 0.7, CENTER)

        send_combo = t_tk.Combobox(self.root,
                                   values=["At most once",
                                           "At least once",
                                           "Exactly once"],
                                   font=("Helvetica", 15),
                                   state="readonly")
        send_combo.current(0)
        send_combo.place(relx=0.2, rely=0.75, anchor=CENTER)
        send_combo.bind("<<ComboboxSelected>>", self.get_selected_action(send_combo))

        self.subscribe_label = f.define_label(self.root, "Subscriptions", 25, FALSE, 0.72, 0.05, CENTER)
        self.subscribe_text = f.define_displayTxt(self.root, width, height, queue)

        done_btn = Button(self.root, text="Done", font=('Helvetica', 16, 'bold'),
                          command=lambda: self.get_entry_text(action_combo, send_combo))
        done_btn.place(relx=0.2, rely=0.85, anchor=CENTER)

        disconnect_btn = Button(self.root, text="Disconnect", font=('Helvetica', 16, 'bold'),
                          command=self.close)
        disconnect_btn.place(relx=0.35, rely=0.9, anchor=CENTER)

    def get_selected_action(self, combobox):
        selected_value = combobox.get()
        self.root.after(500, lambda: self.get_selected_action(combobox))

        return selected_value

    def get_entry_text(self, combobox, combobox2):
        # extragem numele topicului si textul la apasarea butonului "Done"
        action_option = combobox.get()
        topicN_extract = self.topicN_option.get()
        if action_option == "Publish":
            topicT_extract = get_measurements(topicN_extract)
        else:
            topicT_extract = ' '
        send_option = combobox2.get()

        self.topicN_option.delete(0, END)
        self.topicT_entry.delete(0, END)

        self.queue.put(("Main", (action_option, topicN_extract, topicT_extract, send_option)))

    def task_client(self, combobox, topicT_entry):
        option = combobox.get()
        if option == "Subscribe" or option == "Unsubscribe":
            topicT_entry.config(state="disabled")
        if option == "Publish":
            topicT_entry.config(state="disabled") # sau renunțăm de tot la acest câmp
        self.root.after(500, self.task_client, combobox, topicT_entry)

    def update_label(self):
        # aici trebuie sa adaugi text pentru subscribe box
        self.root.update()

    def run(self):
        self.root.mainloop()
        self.update_label()

    def close(self):
        self.queue.put(("Main", ("Disconnect", None, None, None)))
        self.root.withdraw()
        self.root.quit()