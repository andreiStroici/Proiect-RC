from Code.Packet import Packet
from abc import ABC
from Code.FixedHeader import FixedHeader


class CONNACK(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = 32  # tipul pachetului
        self.length = None
        self.__connack_flags = 0
        self.__reason_code = None  # codul care il intoarce server-ul
        self.__property_length = None  # lungimea antetului variabil
        self.__session_expiry_interval_id = 17  # identificatorlui duratei intervalului de expirare a sesiunii
        self.__session_expiry_interval = None  # durata intervalului de expirare a sesiunii in secude
        self.__maximum_receive_id = 33  # identificator pentru maxim de primire
        self.__maximum_receive = None  # valoare identificatorlului maxim de primire
        self.__max_qos_id = 36  # identificatorul pentru QoS maxim
        self.__max_qos = None  # valoarea maxima a QoS
        self.__retain_available_id = 37  # idetificator maxim de primire
        self.__retain_available = None  # valoare maxim de primire
        self.__packet_maximum_size_id = 39  # identificatorul dimensiunii maxime a pachetului
        self.__packet_maximum_size = None  # dimensiunea maxima a dimensiunii maxime a pachetului
        self.__assigned_client_id_id = 18  # identificator pentru id client dat de server
        self.__assigned_client_id = None  # id-ul de client dat de broker
        self.__topic_alias_maximum_id = 34  # identificatorul pentru topic alias maximum
        self.__topic_alias_maximum = None  # valoarea topic alias maximum
        self.__reason_string_id = 31  # identificatorul pentru reason string
        self.__reason_string = None  # valoarea reason string
        self.__user_property_id = 38  # identificatorul prorprietatiilor utilizatorului
        self.__user_property = None  # proprietatiile utilizatorlui
        self.__wildcard_subscription_available_id = 40
        self.__wildcard_subscription_available = None
        self.__subscription_identifiers_id = 42
        self.__subscription_identifiers = None
        self.__shared_subscription_available_id = 42
        self.__shared_subscription_available = None
        self.__server_keep_alive_id = 19
        self.__server_keep_alive = None
        self.__response_information_id = 26
        self.__response_information = None
        self.__server_reference_id = 28
        self.__server_reference = None
        self.__authentication_method_id = 21
        self.__authentication_method = None
        self.__authentication_data_id = 22
        self.__authentication_data = None

    def encode(self) -> str:
        return "Connack: This packet is not send by the client"

    def decode(self, packet) -> str:
        """Prin inetrmediul acestei functii vom decodifica pachetul connect
            si vom verifica si dimensiunea pachetului"""
        if self.type != int(packet[0]):
            return "Malformed packet"
        i = 1  # cu ajutorl lui I voi parcurge pachetul
        lg = 1
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
            lg = lg + 1
        # self.length = packet[1:i + 1]
        self.length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[1:i+1])
        # verific daca lungimea pachetului corespunde cu cea oferita in mesaj
        if self.length != len(packet) - 1 - lg:
            return "Connack: Malformed packet"
        i = i + 1
        self.__connack_flags = packet[i]
        if int(self.__connack_flags) not in [0, 1]:
            return "Connack: Malformed packet"
        i = i + 1
        self.__reason_code = int(packet[i])
        if self.__reason_code not in [0] + list(range(128, 160)):
            return "Connack: Malformed packet"
        i = i + 1
        j = i
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
        self.__property_length = packet[j:i + 1]
        lg, nr_bytes = FixedHeader.decode_variable_byte_integer(self.__property_length)
        # verific lungimea proprietatiilor pachetului
        if lg != len(packet) - i - 1:
            return "Connack: Malformed packet"
        i = i + 1
        maximum = lg + i
        # de acum voi parcurge si voi completa capurile din proprietati
        while i < maximum:
            code = packet[i]
            match code:
                case 17:  # durata expriarii sesiunii
                    i = i + 1
                    if self.__session_expiry_interval is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__session_expiry_interval = packet[i:i + 4]
                        i = i + 4
                    else:
                        return "Connack: Malformed packet"
                case 33:  # maximum receive
                    i = i + 1
                    if self.__maximum_receive is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__maximum_receive = packet[i:i + 2]
                        i = i + 2
                    else:
                        return "Connack: Malformed packet"
                case 36:  # maximum QoS
                    i = i + 1
                    if self.__max_qos is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__max_qos = packet[i]
                        i = i + 1
                    else:
                        return "Connack: Malformed packet"
                case 37:  # ratain available
                    i = i + 1
                    if self.__retain_available is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__retain_available = [i]
                    else:
                        return "Connack: Malformed packet"
                case 39:  # dimensiunea maxima a pachetului
                    i = i + 1
                    if self.__packet_maximum_size is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__packet_maximum_size = packet[i:i + 4]
                        i = i + 4
                    else:
                        return "Connack: Malformed packet"
                case 18:  # identificator de client dat de broker
                    i = i + 1
                    if self.__assigned_client_id is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i + 2]
                        i = i + 2
                        self.__assigned_client_id = str(packet[i:i + length])
                        i = i + length
                    else:
                        return "Connack: Malformed packet"
                case 34:  # topic  alias maximum
                    i = i + 1
                    if self.__topic_alias_maximum is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__topic_alias_maximum = packet[i:i + 2]
                        i = i + 2
                    else:
                        return "Connack: Malformed packet"
                case 31:  # reason string
                    i = i + 1
                    if self.__reason_string is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i+2]
                        i = i + 2
                        self.__reason_string = str(packet[i:i+length])
                        i = i + length
                    else:
                        return "Connack: Malformed packet"
                case 38:  # proprietatiile utilizatorilor
                    i = i + 1
                    if self.__user_property is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i + 2]
                        i = i + 2
                        user_property1 = str(packet[i:i + length])
                        i = i + length
                        length = packet[i:i + 2]
                        i = i + 2
                        user_property2 = str(packet[i:i + length])
                        i = i + length
                        self.__user_property = (user_property1, user_property2)
                    else:
                        return "Connack: Malformed packet"
                case 40:  # wilcard subscribe available
                    i = i + 1
                    if self.__wildcard_subscription_available is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__wildcard_subscription_available = packet[i]
                        i = i + 1
                    else:
                        return "Connack: Malformed packet"
                case 41:  # identificatori de abonare
                    i = i + 1
                    if self.__subscription_identifiers is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__subscription_identifiers = packet[i]
                        i = i + 1
                    else:
                        return "Connack: Malformed packet"
                case 42:  # shared subscription available
                    i = i + 1
                    if self.__shared_subscription_available is None:  # ma asigur ca nu e introdus de 2 ori
                        self.__shared_subscription_available = packet[i]
                        i = i + 1
                    else:
                        return "Connack: Malformed packet"
                case 19:  # server keep alive
                    i = i + 1
                    if self.__server_keep_alive is packet[i:i + 2]:
                        i = i + 2
                    else:
                        return "Connack: Malformed packet"
                case 26:  # response infromation
                    i = i + 1
                    if self.__response_information is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i + 2]
                        i = i + 2
                        self.__response_information = str(packet[i:i + length])
                        i = i + length
                    else:
                        return "Connack: Malformed packet"
                case 28:  # referinta broker
                    i = i + 1
                    if self.__server_reference is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i + 2]
                        i = i + 2
                        self.__server_reference = str(packet[i:i + length])
                        i = i + length
                    else:
                        return "Connack: Malformed packet"
                case 21:  # metoda de autentificare
                    i = i + 1
                    if self.__authentication_method is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i + 2]
                        i = i + 2
                        self.__authentication_method = str(packet[i:i + length])
                        i = i + length
                    else:
                        return "Connack: Malformed packet"
                case 22:  # date de autentificare
                    i = i + 1
                    if self.__authentication_data is None:  # ma asigur ca nu e introdus de 2 ori
                        length = packet[i:i + 2]
                        i = i + 2
                        self.__authentication_data = str(packet[i:i + length])
                        i = i + length
                    else:
                        return "Connack: Malformed packet"
                case _:
                    return "Connack: Malformed packet"
        return "SUCCESS"

    def get_reason_code(self):
        return self.__reason_code

    # Getter pentru property_length
    def get_property_length(self):
        return self.__property_length

    # Getter pentru session_expiry_interval
    def get_session_expiry_interval(self):
        return self.__session_expiry_interval

    # Getter pentru __maximum_receive
    def get_maximum_receive(self):
        return self.__maximum_receive

    # Getter pentru max_qos
    def get_max_qos(self):
        return self.__max_qos

    # Getter pentru retain_available
    def get_retain_available(self):
        return self.__retain_available

    # Getter pentru __packet_maximum_size
    def get_packet_maximum_size(self):
        return self.__packet_maximum_size

    # Getter pentru __assigned_client_id
    def get_assigned_client_id(self):
        return self.__assigned_client_id

    # Getter pentru __topic_alias_maximum
    def get_topic_alias_maximum(self):
        return self.__topic_alias_maximum

    # Getter pentru __user_property
    def get_user_property(self):
        return self.__user_property

    # Getter pentru __wildcard_subscription_available
    def get_wildcard_subscription_available(self):
        return self.__wildcard_subscription_available

    # Getter pentru __subscription_identifiers
    def get_subscription_identifiers(self):
        return self.__subscription_identifiers

    # Getter pentru __server_keep_alive
    def get_server_keep_alive(self):
        return self.__server_keep_alive

    # Getter pentru __response_information
    def get_response_information(self):
        return self.__response_information

    # Getter pentru __server_reference
    def get_server_reference(self):
        return self.__server_reference

    # Getter pentru __authentication_method
    def get_authentication_method(self):
        return self.__authentication_method

    # Getter pentru __authentication_data
    def get_authentication_data(self):
        return self.__authentication_data
