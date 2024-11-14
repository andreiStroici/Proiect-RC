from Functions import *

def connect_interface():
    def get_entry_text():
        # extragem username-ul și parola la apăsarea butonului "Login"
        name_extract = name_entry.get()
        pass_extract = pass_entry.get()

        print("Extracted name:", name_extract)
        print("Extracted password:", pass_extract)

    root = Tk()
    root.title("MQTT Client")
    root.geometry("600x500")

    define_label(root, "Client Connect Interface", 18, TRUE, 0.5, 0.10, CENTER)

    define_label(root, "Username", 16, FALSE, 0.5, 0.25, CENTER)
    name_entry = define_entry(root, FALSE, 0.5, 0.30)

    define_label(root, "Password", 16, FALSE, 0.5, 0.45, CENTER)
    pass_entry = define_entry(root, TRUE, 0.5, 0.5)

    login_btn = Button(root, text="Login", font=('Helvetica', 16, 'bold'), command=get_entry_text)
    login_btn.place(relx=0.5, rely=0.65, anchor=CENTER)

    root.mainloop()


connect_interface()
