import multiprocessing
from multiprocessing import Process, Pipe
from Code.Client import  Client


def main():
    """Aceasta este functia main cu thread-ul prinicipal al aplicatiei
    Aici vom crea si thread-ul pentru client
    Ea nu are niciun raspuns"""
    queue = multiprocessing.Queue()
    username = input("usenrame:\n")
    password = input("password:\n")
    client = Client("localhost", 1883, queue)
    client.set_username(username)
    client.set_password(password)
    client_proc = Process(target=client.operation)
    client_proc.start()
    while True:
        if not queue.empty():
            destination, message = queue.get()
            if destination != "Main":
                queue.put((destination, message))
            else:
                # if message == "Hello":
                #     print("Buna din main")
                # elif message == "M-am plictisit":
                #     queue.put(("Client", "Terminate"))
                # elif message == "SIGKILL Receive":
                #     client_proc.terminate()
                #     break
                # vom lucra cu mesajul trimis
                pass
    client_proc.join()
    print("Termianre")


if __name__ == "__main__":
    main()
