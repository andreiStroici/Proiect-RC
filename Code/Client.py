import os
import random
import socket

from getmac import get_mac_address


class Client:
    def __init__(self, broker_ip, broker_port):
        # acestea sunt informatiile clientului
        self.__client_id = self.generate_client_id()
        self.__username = None
        self.__password = None
        # este pus decoamdata pe None, deoarece valoarea lui va fi setata cand se va trimite CONNECT
        # atuncti vom trimite si timpul pt keep alive
        self.__timer = None
        # pastrez ip-ul si portul brokerului pentru a sti unde voi trimite pachetele
        self.__broker_ip = broker_ip
        self.__broker_port = broker_port
        # acest atribut va pastra ultimul pachet trimis
        self.__packet = None
        # acest atribut va pastra calitatea srviciului, by default va fi 0
        self.__QoS = 0

    @staticmethod
    def generate_client_id(self):
        try:
            device_name = os.environ.get('COMPUTERNAME')

            # Remove hyphens and strip whitespace
            device_name = device_name.replace('-', '').strip()  # șterg caracterul '-' din numele dispozitvului
            if not device_name:
                device_name = "Unkonwn" + random.randint(0, 100)
            unique_id = str(get_mac_address().replace(":", "")[-8:])  # Use 8 characters for better uniqueness

            return f"{device_name}{unique_id}"

        except Exception as e:
            print(f"Error generating client ID: {str(e)}")
            return None

    def send_message(self, type):
        packet = Packet()
        match type:
            case "CONNECT":
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
                # trebuie gasit o solutie daca cumva apar erori la trimiterea tipului de pachet
                pass
        self.__packet = packet

    def receive_message(self):
        s_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_conn.connect((self.__broker_ip, self.__broker_ip))
        # extragem primii 4 biti din pachet pentru a vedea tipul pachetului
        while True:
            data = s_conn.recv(268435455)
            first_4_bits = (data[0] >> 4) & 0x0F
            match first_4_bits:
                case 2:
                    # CONNACK
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

    def operation(self):
        # in interiorul acestei functii va fi ca un main pt client
        # el va monitoriza timerele si va comunica cu Receive si Main
        pass

    # Getter și setter pentru client_id
    def get_client_id(self):
        # Returnează ID-ul clientului.
        return self.__client_id

    # Getter și setter pentru username
    def get_username(self):
        #Returnează numele de utilizator.#
        return self.__username

    def set_username(self, username):
        #Setează numele de utilizator."""
        self.__username = username

    # Getter și setter pentru password
    def get_password(self):
        #Returnează parola.
        return self.__password

    def set_password(self, password):
        #Setează parola.
        self.__password = password

    # Getter și setter pentru timer
    def get_timer(self):
        #Returnează timpul pentru keep alive.
        return self.__timer

    def set_timer(self, timer):
        #Setează timpul pentru keep alive.
        self.__timer = timer

    # Getter și setter pentru broker_ip
    def get_broker_ip(self):
        #Returnează adresa IP a brokerului.
        return self.__broker_ip

    def set_broker_ip(self, broker_ip):
        #Setează adresa IP a brokerului.
        self.__broker_ip = broker_ip

    # Getter și setter pentru broker_port
    def get_broker_port(self):
        #Returnează portul brokerului.
        return self.__broker_port

    def set_broker_port(self, broker_port):
        #Setează portul brokerului.
        self.__broker_port = broker_port

    # Getter și setter pentru packet
    def get_packet(self):
        #Returnează ultimul pachet trimis.
        return self.__packet

    def set_packet(self, packet):
        #Setează ultimul pachet trimis.
        self.__packet = packet

    # Getter și setter pentru QoS
    def get_QoS(self):
        #Returnează calitatea serviciului (QoS).
        return self.__QoS

    def set_QoS(self, QoS):
        #Setează calitatea serviciului (QoS).
        self.__QoS = QoS

