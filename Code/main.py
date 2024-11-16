import multiprocessing
from multiprocessing import Process, Pipe
from Code.Client import  Client
from Client_Connect_Interface import *

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
    try:
        while True:
            if not queue.empty():
                destination, message = queue.get()
                if destination != "Main":
                    queue.put((destination, message))
                else:
                    if message == "Terminate":
                        client_proc.terminate()
                        break
                    pass
        client_proc.join()
        print("Termianre")
    except BaseException:
        print("Inchidere brusca a aplicatiei")


if __name__ == "__main__":
    main()
