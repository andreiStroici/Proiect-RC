import multiprocessing
import threading
from multiprocessing import Process, Pipe
from Code.Client import  Client
from Client_Connect_Interface import *
from Client_Interface import *

def run_client_interface(queue):
    client = Client_Interface(queue)
    client.run()

def main():
    """Aceasta este functia main cu thread-ul prinicipal al aplicatiei
    Aici vom crea si thread-ul pentru client
    Ea nu are niciun raspuns"""
    queue = multiprocessing.Queue()

    #username = "proba1"
    #password = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    connect_interface(queue)
    username, password = queue.get()
    print("Sunt in main acum: ")
    print("Username: ", username)
    print("Password: ", password)

    client = Client("127.0.0.1", 1883, queue)
    client.set_username(username)
    client.set_password(password)
    client_proc = Process(target=client.operation)
    client_proc.start()

    client_interface_thread = threading.Thread(target=run_client_interface, args=(queue,))
    client_interface_thread.start()

    try:
        while True:
            destination = None
            message = None
            while True:
                try:
                    destination, message = queue.get()
                    break
                except queue.empty:
                    continue
            if destination != "Main":
                queue.put((destination, message))
            else:
                if isinstance(message, tuple):
                    print(message)
                elif message == "Terminate":
                    client_proc.terminate()
                    break
                elif "Malformed" in message:
                    print(f"There is an error received from broker {message}.")
                    client_proc.terminate()
                    break
    except BaseException:
        print("The application suddenly stopped.")
    finally:
        client_interface_thread.join()
        client_proc.join()
        print("The app is closing.")


if __name__ == "__main__":
    main()
