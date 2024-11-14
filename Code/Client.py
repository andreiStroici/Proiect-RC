import multiprocessing
import os
import random
import socket
from multiprocessing import Process
from Code.ImportFile import *
from getmac import get_mac_address


class Client:
    def __init__(self, broker_ip, broker_port, queue: multiprocessing.Queue):
        """Inițializează un obiect MQTTClient cu IP-ul și portul brokerului.

        Atributele includ ID-ul clientului generat automat, numele de utilizator și parola,
        timpul de keep alive (inițial None), IP-ul și portul brokerului, ultimul pachet trimis,
        și calitatea serviciului (QoS), care este setată implicit la 0.
        """

        self.__client_id = "mqttx_c2718eb2"
        # self.__client_id = self.generate_client_id()
        self.__username = None
        self.__password = None
        self.__timer = None  # Va fi setat când se trimite pachetul CONNECT
        self.__broker_ip = broker_ip  # IP-ul brokerului MQTT
        self.__broker_port = broker_port  # Portul brokerului MQTT
        self.s_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creez un obiect de tip socket
        self.s_conn.connect((self.__broker_ip, self.__broker_port))  # realizez conexiunea cu serverul
        self.__packet = None  # Ultimul pachet trimis
        self.__QoS = 0  # Calitatea serviciului, implicit 0
        self.queue = queue  # Coada de mesaje folosita pt comunicarea intre thread-uri

    @staticmethod
    def generate_client_id():
        """Generează un ID unic pentru client, bazat pe numele dispozitivului și adresa MAC.

        Returns:
            str: ID-ul unic al clientului sau None dacă apare o eroare.
        """
        try:
            device_name = os.environ.get('COMPUTERNAME')
            if device_name:
                device_name = device_name.replace('-', '').strip()
            else:
                device_name = f"Unknown{random.randint(0, 100)}"
            unique_id = str(get_mac_address().replace(":", "")[-8:])  # Ultimele 8 caractere pentru unicitate
            return f"{device_name}{unique_id}"
        except Exception as e:
            print(f"Error generating client ID: {str(e)}")
            return None

    def send_message(self, packet_type):
        """Trimite un mesaj de tip specific către broker.

        Args:
            type (str): Tipul pachetului (ex. CONNECT, PUBLISH, SUBSCRIBE, etc.).

        Note:
            Acestă metodă setează atributul __packet cu un pachet corespunzător.
            Momentan, tipurile de pachete nu sunt implementate.
            :param packet_type:
        """
        match packet_type:
            case "CONNECT":
                self.__packet = CONNECT()
                self.__packet.set_will_property_length(0)
                self.__packet.set_client_id(self.__client_id)
                self.__packet.set_username(self.__username)
                self.__packet.set_password(self.__password)
                encoded_packet = self.__packet.encode()
                self.s_conn.send(encoded_packet.encode())
                pass
            case "PUBLISH":
                pass
            case "PUBACK":
                pass
            case "PUBREC":
                pass
            case "PUBREL":
                pass
            case "PUBCOMP":
                pass
            case "SUBSCRIBE":
                pass
            case "UNSUBSCRIBE":
                pass
            case "PINGREQ":
                pass
            case "DISCONNECT":
                pass
            case _:
                # Trebuie găsită o soluție pentru erorile la tipurile de pachete
                pass
        print("End send")

    def receive_message(self):
        """Primește un mesaj de la broker și determină tipul pachetului.

        Note:
            Metoda folosește socket-uri pentru a stabili conexiunea cu brokerul.
            Extrage primii 4 biți din datele primite pentru a determina tipul pachetului.
        """
        # while True:
        #     destination = "Main"
        #     var = "M-am plictisit"
        #     message = (destination, var)
        #     self.queue.put(message)
        #     #print(f"Receive a trimis:{var}, la {destination}")
        #self.s_conn.settimeout(10.0)
        try:
            while True:
                data = self.s_conn.recv(1024)
                if not data:
                    self.queue.put(("Client", "Terminate"))
                    break
                first_4_bits = (data[0] >> 4) & 0x0F
                match first_4_bits:
                    case 2:
                        # CONNACK
                        print(self.__packet.get_reason_code())
                        match self.__packet.get_reason_code():
                            case 0:
                                print("Success")
                            case 128:
                                print("Unspecified error")
                            case 129:
                                print("Malformed Packet")
                            case 130:
                                print("Protocol Error")
                            case 131:
                                print("Implementation specific error")
                            case 132:
                                print("Unsupported Protocol Version")
                            case 133:
                                print("Client Identifier not valid")
                            case 134:
                                print("Bad User Name or Password")
                            case 135:
                                print("Not authorized")
                            case 136:
                                print("Server unavailable")
                            case 137:
                                print("Server busy")
                            case 138:
                                print("Banned")
                            case 140:
                                print("Bad authentication method")
                            case 144:
                                print("Topic Name invalid")
                            case 149:
                                print("Packet too large")
                            case 151:
                                print("Quota exceeded")
                            case 153:
                                print("Payload format invalid")
                            case 154:
                                print("Retain not supported")
                            case 155:
                                print("QoS not supported")
                            case 156:
                                print("Use another server")
                            case 157:
                                print("Server moved")
                            case 159:
                                print("Connection rate exceeded")
                        pass
                    case 3:
                        # PUBLISH
                        pass
                    case 4:
                        # PUBACK
                        pass
                    case 5:
                        # PUBREC
                        pass
                    case 6:
                        # PUBREL
                        pass
                    case 7:
                        # PUBCOMP
                        pass
                    case 9:
                        # SUBACK
                        pass
                    case 11:
                        # UNSUBACK
                        pass
                    case 13:
                        # PINGRESP
                        pass
                    case 14:
                        # DISCONNECT
                        pass
        except BaseException:
            print("Eroare de la primirea pachetelor")

    def operation(self):
        """ in interiorul acestei functii va fi ca un main pt client
         el va monitoriza timerele si va comunica cu Receive si Main dar
         va si creea thread-ul Receive"""
        receive = Process(target=self.receive_message)
        receive.start()
        self.send_message("CONNECT")
        while True:
            if not self.queue.empty():
                destination, message = self.queue.get()
                if destination != "Client":
                    self.queue.put((destination, message))
                else:
                    if message == "Terminate":
                        receive.terminate()
                        receive.join()
                        self.queue.put(("Main", "Terminate"))
        # pass

    # Getter și setter pentru client_id
    def get_client_id(self):
        """Returnează ID-ul clientului."""
        return self.__client_id

    # Getter și setter pentru username
    def get_username(self):
        """Returnează numele de utilizator."""
        return self.__username

    def set_username(self, username):
        """Setează numele de utilizator."""
        self.__username = username

    # Getter și setter pentru password
    def get_password(self):
        """Returnează parola."""
        return self.__password

    def set_password(self, password):
        """Setează parola."""
        self.__password = password

    # Getter și setter pentru timer
    def get_timer(self):
        """Returnează timpul pentru keep alive."""
        return self.__timer

    def set_timer(self, timer):
        """Setează timpul pentru keep alive."""
        self.__timer = timer

    # Getter și setter pentru broker_ip
    def get_broker_ip(self):
        """Returnează adresa IP a brokerului."""
        return self.__broker_ip

    def set_broker_ip(self, broker_ip):
        """Setează adresa IP a brokerului."""
        self.__broker_ip = broker_ip

    # Getter și setter pentru broker_port
    def get_broker_port(self):
        """Returnează portul brokerului."""
        return self.__broker_port

    def set_broker_port(self, broker_port):
        """Setează portul brokerului."""
        self.__broker_port = broker_port

    # Getter și setter pentru packet
    def get_packet(self):
        """Returnează ultimul pachet trimis."""
        return self.__packet

    def set_packet(self, packet):
        """Setează ultimul pachet trimis."""
        self.__packet = packet

    # Getter și setter pentru QoS
    def get_QoS(self):
        """Returnează calitatea serviciului (QoS)."""
        return self.__QoS

    def set_QoS(self, QoS):
        """Setează calitatea serviciului (QoS)."""
        self.__QoS = QoS
