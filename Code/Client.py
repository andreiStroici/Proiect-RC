import multiprocessing
import os
import queue
import random
import socket
import time
from multiprocessing import Process, Lock, Manager

from Code.DISCONNECT import DISCONNECT
from Code.ImportFile import *
from getmac import get_mac_address


class Client:
    def __init__(self, broker_ip, broker_port, queue: multiprocessing.Queue):
        """Inițializează un obiect MQTTClient cu IP-ul și portul brokerului.
        Atributele includ ID-ul clientului generat automat, numele de utilizator și parola,
        timpul de keep alive (inițial None), IP-ul și portul brokerului, ultimul pachet trimis,
        și calitatea serviciului (QoS), care este setată implicit la 0.
        """

        # self.__client_id = "mqttx_28f24124"
        self.__client_id = self.generate_client_id()
        self.__username = None
        self.__password = None
        self.__timer = None  # retine momentul la care am trimis pachetul
        self.__broker_ip = broker_ip  # IP-ul brokerului MQTT
        self.__broker_port = broker_port  # Portul brokerului MQTT
        self.s_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creez un obiect de tip socket
        self.s_conn.connect((self.__broker_ip, self.__broker_port))  # realizez conexiunea cu serverul
        self.__packet = None  # Ultimul pachet trimis
        self.__QoS = 0  # Calitatea serviciului, implicit 0
        self.queue = queue  # Coada de mesaje folosita pt comunicarea intre pocese
        self.__last_topic_filter = []  # aici voi tine ultimele topic filters trimise prin subscribe
        self.__last_packet_identifier = None
        # aici voi tine ultimele topic filters trimise prin subscribe
        self.__receive_queue = multiprocessing.Queue()  # coada de mesaje folosita pentru coerenta datelor intre procese
        self.__topic_message = None

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
                self.__packet.set_client_id(self.__client_id)
                self.__packet.set_username(self.__username)
                self.__packet.set_password(self.__password)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, "big"))
                self.s_conn.send(var)
                pass
            case "PUBLISH":
                self.__packet = PUBLISH()
                self.__packet.set_QoS(self.__QoS)
                self.__packet.set_topic_name(self.__last_topic_filter[0])
                if self.__QoS > 0:
                    last_packet_id = random.randint(0, 65636)
                    self.__last_packet_identifier = last_packet_id
                    self.__packet.set_packet_identifier(self.__last_packet_identifier)
                    self.__receive_queue.put(self.__last_packet_identifier)
                self.__packet.set_message(self.__topic_message)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, "big"))
                self.s_conn.send(var)
                pass
            case "PUBACK":
                self.__packet = PUBACK()
                self.__packet.set_packet_identifier(self.__last_packet_identifier)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, 'big'))
                self.s_conn.send(var)
                pass
            case "PUBREC":
                self.__packet = PUBREC()
                self.__packet.set_packet_identifier(self.__last_packet_identifier)
                self.__receive_queue.put(self.__last_packet_identifier)
                self.__packet.set_reason_code(0)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, 'big'))
                self.s_conn.send(var)
                pass
            case "PUBREL":
                self.__packet = PUBREL()
                self.__packet.set_packet_identifier(self.__last_packet_identifier)
                self.__receive_queue.put(self.__last_packet_identifier)
                self.__packet.set_reason_code(0)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, 'big'))
                self.s_conn.send(var)
                pass
            case "PUBCOMP":
                self.__packet = PUBCOMP()
                self.__packet.set_packet_identifier(self.__last_packet_identifier)
                self.__packet.set_reason_code(0)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, 'big'))
                self.s_conn.send(var)
                pass
            case "SUBSCRIBE":
                self.__packet = SUBSCRIBE()
                self.__packet.set_topic_filters(self.__last_topic_filter)
                self.__packet.set_subscription_options(self.__QoS)
                self.__last_topic_filter = self.__packet.get_topic_filters()
                last_packet_id = random.randint(0, 65636)
                self.__last_packet_identifier = last_packet_id
                self.__packet.set_packet_identifier(self.__last_packet_identifier)
                self.__receive_queue.put((self.__last_topic_filter, self.__last_packet_identifier))
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, "big"))
                self.s_conn.send(var)
                pass
            case "UNSUBSCRIBE":
                self.__packet = UNSUBSCRIBE()
                last_packet_id = random.randint(0, 65636)
                self.__packet.set_packet_identifier(last_packet_id)
                self.__last_packet_identifier = last_packet_id
                self.__packet.set_topic_filter(self.__last_topic_filter)
                self.__receive_queue.put((self.__last_topic_filter, self.__last_packet_identifier))
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, "big"))
                self.s_conn.send(var)
                pass
            case "PINGREQ":
                self.__packet = PINGREQ()
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, "big"))
                self.s_conn.send(var)
                pass
            case "DISCONNECT":
                self.__packet = DISCONNECT()
                self.__packet.set_reason_code(0x00)
                self.__packet.set_reason_string("Client requested disconnect")
                self.__packet.set_session_expiring_interval(0)
                encoded_packet = self.__packet.encode()
                var = bytearray()
                for byte in encoded_packet:
                    var.extend(ord(byte).to_bytes(1, byteorder="big"))
                self.s_conn.send(var)
                pass
            case _:
                # Trebuie găsită o soluție pentru erorile la tipurile de pachete
                pass
        self.__timer = time.time()

    def receive_message(self):
        """Primește un mesaj de la broker și determină tipul pachetului.

        Note:
            Metoda folosește socket-uri pentru a stabili conexiunea cu brokerul.
            Extrage primii 4 biți din datele primite pentru a determina tipul pachetului.
        """
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
                        self.__packet = CONNACK()
                        is_correct = self.__packet.decode(data)
                        if is_correct != "SUCCESS":
                            print("Malformed CONNACK")
                            self.queue.put(("Client", "Malformed CONNACK"))
                        match self.__packet.get_reason_code():
                            case 0:
                                print("Connack: Success")
                            case 128:
                                print("Connack: Unspecified error")
                            case 129:
                                print("Connack: Malformed Packet")
                            case 130:
                                print("Connack: Protocol Error")
                            case 131:
                                print("Connack: Implementation specific error")
                            case 132:
                                print("Connack: Unsupported Protocol Version")
                            case 133:
                                print("Connack: Client Identifier not valid")
                            case 134:
                                print("Connack: Bad User Name or Password")
                            case 135:
                                print("Connack: Not authorized")
                            case 136:
                                print("Connack: Server unavailable")
                            case 137:
                                print("Connack: Server busy")
                            case 138:
                                print("Connack: Banned")
                            case 140:
                                print("Connack: Bad authentication method")
                            case 144:
                                print("Connack: Topic Name invalid")
                            case 149:
                                print("Connack: Packet too large")
                            case 151:
                                print("Connack: Quota exceeded")
                            case 153:
                                print("Connack: Payload format invalid")
                            case 154:
                                print("Connack: Retain not supported")
                            case 155:
                                print("Connack: QoS not supported")
                            case 156:
                                print("Connack: Use another server")
                            case 157:
                                print("Connack: Server moved")
                            case 159:
                                print("Connack: Connection rate exceeded")
                        pass
                    case 3:
                        # PUBLISH
                        self.__packet = PUBLISH()
                        self.__packet.set_topic_name(self.__last_topic_filter[0])
                        self.__packet.set_packet_identifier(self.__last_packet_identifier)
                        self.__packet.set_message(self.__topic_message)
                        is_correct = self.__packet.decode(data)
                        if is_correct != "SUCCESS":
                            print(f"Malformed PUBLISH {is_correct}")
                            self.queue.put(("Client", "Malformed PUBLISH"))
                        else:
                            if self.__packet.get_QoS() == 1:
                                self.queue.put(("Client", ("Puback", str(self.__packet.get_packet_identifier()), str(self.__packet.get_QoS()))))
                            elif self.__packet.get_QoS() == 2:
                                self.queue.put(("Client", ("Pubrec", str(self.__packet.get_packet_identifier()), str(self.__packet.get_QoS()))))
                        # print("RECEIVED PUBLISH: ")
                        # print(f"QoS: {self.__packet.get_QoS()}")
                        # print(f"Packet identifier: {self.__packet.get_packet_identifier()}")
                        # print(f"topic: {self.__packet.get_topic_name()}")
                        # print(f"message: {self.__packet.get_message()}")
                        self.queue.put(("Interface", (self.__packet.get_topic_name(), self.__packet.get_message())))
                        pass
                    case 4:
                        # PUBACK
                        while True:
                            try:
                                message = self.__receive_queue.get(
                                    timeout=1)  # Așteaptă până la 1 secundă pentru a primi un mesaj
                                if message is None:
                                    continue
                                self.__last_packet_identifier = message
                                break
                            except queue.Empty:
                                # Tratează cazurile în care coada este goală după timeout
                                continue
                        self.__packet = PUBACK()
                        self.__packet.set_last_packet_identifier(self.__last_packet_identifier)
                        is_correct, message_reason_code = self.__packet.decode(data)
                        if is_correct != "SUCCESS":
                            print(f"PUBACK {is_correct}")
                            self.queue.put(("Client", "Malformed PUBACK"))
                        else:
                            if message_reason_code != 'Success':
                                self.queue.put(("Interface", ('PUBACK', message_reason_code)))
                        pass
                    case 5:
                        # PUBREC
                        while True:
                            try:
                                message = self.__receive_queue.get(
                                    timeout=1)  # Așteaptă până la 1 secundă pentru a primi un mesaj
                                if message is None:
                                    continue
                                self.__last_packet_identifier = message
                                break
                            except queue.Empty:
                                # Tratează cazurile în care coada este goală după timeout
                                continue
                        self.__packet = PUBREC()
                        self.__packet.set_last_packet_identifier(self.__last_packet_identifier)
                        is_correct, message_reason_code = self.__packet.decode(data)
                        if "Malformed" in is_correct:
                            print(f"PUBREC {is_correct}")
                            self.queue.put(("Client", "Malformed PUBREC"))
                        else:
                            if message_reason_code != 'Success':
                                self.queue.put(("Interface", ('PUBREC', message_reason_code)))
                            else:
                                self.queue.put(("Client", ("Pubrel", str(self.__last_packet_identifier))))
                        pass
                    case 6:
                        # PUBREL
                        while True:
                            try:
                                message = self.__receive_queue.get(
                                    timeout=1)  # Așteaptă până la 1 secundă pentru a primi un mesaj
                                if message is None:
                                    continue
                                self.__last_packet_identifier = message
                                break
                            except queue.Empty:
                                # Tratează cazurile în care coada este goală după timeout
                                continue
                        self.__packet = PUBREL()
                        self.__packet.set_last_packet_identifier(self.__last_packet_identifier)
                        is_correct, message_reason_code = self.__packet.decode(data)
                        if "Malformed" in is_correct:
                            print(f"PUBREC {is_correct}")
                            self.queue.put(("Client", "Malformed PUBREC"))
                        else:
                            if message_reason_code != 'Success':
                                self.queue.put(("Interface", ('PUBREL', message_reason_code)))
                            else:
                                self.queue.put(("Client", ("Pubcomp", str(self.__last_packet_identifier))))
                        pass
                    case 7:
                        # PUBCOMP
                        while True:
                            try:
                                message = self.__receive_queue.get(
                                    timeout=1)  # Așteaptă până la 1 secundă pentru a primi un mesaj
                                if message is None:
                                    continue
                                self.__last_packet_identifier = message
                                break
                            except queue.Empty:
                                # Tratează cazurile în care coada este goală după timeout
                                continue
                        self.__packet = PUBCOMP()
                        self.__packet.set_last_packet_identifier(self.__last_packet_identifier)
                        is_correct, message_reason_code = self.__packet.decode(data)
                        if "Malformed" in is_correct:
                            print(f"PUBCOMP {is_correct}")
                            self.queue.put(("Client", "Malformed PUBCOMP"))
                        else:
                            if message_reason_code != 'Success':
                                self.queue.put(("Interface", ('PUBCOMP', message_reason_code)))
                            else: print("PUBLISH with QoS2 successfully sent.")
                        pass
                    case 9:
                        # SUBACK
                        # it = 0
                        while True:
                            try:
                                message = self.__receive_queue.get(
                                    timeout=1)  # Așteaptă până la 1 secundă pentru a primi un mesaj
                                if message is None:
                                    continue
                                self.__last_topic_filter = message[0]
                                self.__last_packet_identifier = message[1]
                                break
                            except queue.Empty:
                                # Tratează cazurile în care coada este goală după timeout
                                continue
                        self.__packet = SUBACK()
                        self.__packet.set_last_packet_identifier(self.__last_packet_identifier)
                        self.__packet.set_topic_filters(self.__last_topic_filter)
                        is_correct = self.__packet.decode(data)
                        if is_correct != "SUCCESS":
                            print(f"SUBACK {is_correct}")
                            self.queue.put(("Client", "Malformed SUBACK"))
                        pass
                    case 11:
                        # UNSUBACK
                        while True:
                            try:
                                message = self.__receive_queue.get(
                                    timeout=1)  # Așteaptă până la 1 secundă pentru a primi un mesaj
                                if message is None:
                                    continue
                                self.__last_topic_filter = message[0]
                                self.__last_packet_identifier = message[1]
                                break
                            except queue.Empty:
                                # Tratează cazurile în care coada este goală după timeout
                                continue
                        self.__packet = UNSUBACK()
                        self.__packet.set_last_packet_id(self.__last_packet_identifier)
                        self.__packet.set_topic_filters(self.__last_topic_filter)
                        is_correct = self.__packet.decode(data)
                        if is_correct != "SUCCESS":
                            print(f"UNSUBACK: {is_correct}")
                            self.queue.put(("Client", "Malformed UNSUBACK"))
                        pass
                    case 13:
                        # PINGRESP
                        self.__packet = PINGRESP()
                        is_correct = self.__packet.decode(data)
                        if is_correct != "SUCCESS":
                            print("Malformed PINGRESP")
                            self.queue.put(("Client", "Malformed PINGRESP"))
                        pass
                    case 14:
                        # DISCONNECT
                        self.__packet = DISCONNECT()
                        is_correct = self.__packet.decode(data)
                        if is_correct != "SUCCES":
                            print("Malformed DISCONNECT")
                            self.queue.put(("Client", "Malformed DISCONNECT"))
                        pass
        except BaseException as e:
            print("Eroare de la primirea pachetelor")
            print(e)
            self.queue.put(("Interfata", "Terminate"))
            self.queue.put(("Client", "Terminate"))

    def operation(self):
        """ in interiorul acestei functii va fi ca un main pt client
         el va monitoriza timerele si va comunica cu Receive si Main dar
         va si creea thread-ul Receive"""
        receive = Process(target=self.receive_message)
        receive.start()

        self.send_message("CONNECT")
        while True:
            try:
                if not self.queue.empty():
                    destination, message = self.queue.get()
                    if destination != "Client":
                        self.queue.put((destination, message))
                    else:
                        if message == "Terminate":
                            receive.terminate()
                            receive.join()
                            self.queue.put(("Main", "Terminate"))
                        if "Malformed" in message:
                            receive.terminate()
                            receive.join()
                            self.queue.put("Main", message)
                        if isinstance(message, tuple):
                            if message[1] is not None:
                                self.__last_topic_filter = message[1].split(', ')
                            match message[0]:
                                case "Publish":
                                    self.__topic_message = message[2]
                                    match message[3]:
                                        case "At least once":
                                            self.__QoS = 1
                                        case "Exactly once":
                                            self.__QoS = 2
                                        case "At most once":
                                            self.__QoS = 0
                                    self.send_message("PUBLISH")
                                    print("SEND PUBLISH")
                                case "Puback":
                                    self.__last_packet_identifier = int(message[1])
                                    self.__QoS = int(message[2])
                                    self.send_message("PUBACK")
                                    print("SEND PUBACK")
                                case "Pubrec":
                                    self.__last_packet_identifier = int(message[1])
                                    self.__QoS = int(message[2])
                                    self.send_message("PUBREC")
                                    print("SEND PUBREC")
                                case "Pubrel":
                                    self.__last_packet_identifier = int(message[1])
                                    self.send_message("PUBREL")
                                    print("SEND PUBREL")
                                case "Pubcomp":
                                    self.__last_packet_identifier = int(message[1])
                                    self.send_message("PUBCOMP")
                                    print("SEND PUBCOMP")
                                case "Subscribe": # ramane sa modificam cu tipul de QoS
                                    match message[3]:
                                        case "At least once":
                                            self.__QoS = 1
                                        case "Exactly once":
                                            self.__QoS = 2
                                        case "At most once":
                                            self.__QoS = 0
                                    self.send_message("SUBSCRIBE")
                                    print("SEND SUBSCRIBE")
                                case "Unsubscribe":
                                    self.send_message("UNSUBSCRIBE")
                                    print("SEND UNSUBSCRIBE")
                                case "Disconnect":
                                    self.send_message("DISCONNECT")
                                    print("SEND DISCONNECT")
                                    self.queue.put(("Client", "Terminate"))
            except queue.Empty:
                continue
            finally:
                if time.time() - self.__timer > 60:
                    self.send_message("PINGREQ")
                    print("SEND PING")

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
