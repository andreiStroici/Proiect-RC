import multiprocessing
from multiprocessing import Process
from Code.Client import Client
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

    connect_interface(queue)
    status, (username, password) = queue.get()
    if status == "Abort":
        print("The app is closing.")
        return 0

    client = Client("127.0.0.1", 1883, queue)
    client.set_username(username)
    client.set_password(password)
    client_proc = Process(target=client.operation)
    client_proc.start()

    client_interface_proc = Process(target=run_client_interface, args=(queue,))
    client_interface_proc.start()

    try:
        while True:
            try:
                destination = None
                message = None
                destination, message = queue.get()
                if destination != "Main":
                    queue.put((destination, message))
                else:
                    if isinstance(message, tuple):
                        queue.put(("Client", message))
                    elif message == "Terminate":
                        client_interface_proc.terminate()
                        client_proc.terminate()
                        break
                    elif "Malformed" in message:
                        print(f"There is an error received from broker {message}.")
                        client_proc.terminate()
                        break
            except queue.empty:
                continue

    except BaseException:
        print("The application suddenly stopped.")
    finally:
        client_interface_proc.join()
        client_proc.join()
        print("The app is closing.")


if __name__ == "__main__":
    main()
