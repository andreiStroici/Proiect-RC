import struct
from abc import ABC
import numpy as np
from Code.FixedHeader import FixedHeader
from Code.Packet import Packet


class CONNECT(Packet, ABC):
    def __init__(self):
        """Vom crea obiectul care va descrie pachetul CONNECT
        inculzand toate informatiile pachetului
        Antetul fix e mostenit"""
        super().__init__()
        self.type = np.uint8(16)
        self.length = None
        self.__byte = np.uint16(4)  # cei 2 octeti inaintea numelui protocolului
        self.__name = "MQTT"  # numele protocolului
        self.__protocol_version = np.uint8(5)  # verisunea protocolului
        self.__flags = np.uint8(194)  # flag-urile folosite
        # self.__keep_alive = np.uint16(60)  # durata intervalului de keep alive
        self.__keep_alive = 60  # durata intervalului de keep alive
        self.__property_length = None  # lunginea proprietatiilor pachetlui
        self.__session_expiry_interval_id = np.uint8(17)  # identifiactorul duratei de expirare a intervalului
        self.__session_expiry_interval = None  # durata de expirare a intervalului in secude
        self.__maximum_receive_id = np.uint8(33)  # identificator pentru maxim de primire
        self.__maximum_receive = None  # valoare identificatorlului maxim de primire
        self.__packet_maximum_size_id = np.uint8(39)  # identificatorul dimensiunii maxime a pachetului
        self.__packet_maximum_size = None  # dimensiunea maxima a dimensiunii maxime a pachetului
        self.__topic_alias_maximum_id = np.uint8(34)  # identificatorul pentru topic alias maximum
        self.__topic_alias_maximum = None  # valoarea topic alias maximum
        self.__request_response_information_id = np.uint8(25)  # identificator cerere pentru informații despre răspuns
        self.__request_response_information = None  # cerere pentru informații despre răspuns
        self.__request_problem_information_id = np.uint8(23)  # identificator solicitare informații despre erori
        self.__request_problem_information = None  # solicitare informații despre erori
        self.__user_property_id = np.uint8(38)  # identificatorul prorprietatiilor utilizatorului
        self.__user_property = None  # proprietatiile utilizatorlui
        self.__authentication_method_id = np.uint8(21)  # identificatorul metodei de autentificare
        self.__authentication_method = None  # metoda de autentificare
        self.__authentication_data_id = np.uint8(22)  # identifiacatorul datelor de autentificare
        self.__authentication_data = None  # datele de autentificare
        self.__client_id = None  # identificatorul clientului
        self.__will_property_length = None  # lungimea proprietatii will
        self.__will_delay_interval_id = np.uint8(24)  # identificator intervalului de delay will
        self.__will_delay_interval = None  # valoare intervalului de delay will in secunde
        self.__payload_format_indicator_id = np.uint8(1)  # identificator format payload indicator
        self.__payload_format_indicator = None  # valoare fromat payload identificator
        self.__message_expiring_interval_id = np.uint8(2)  # identificator durata expirare mesaj
        self.__message_expiring_interval = None  # valoare expirare interval in secunde
        self.__content_type_id = np.uint8(3)  # identificator tip de contiunt
        self.__content_type = None  # tipul contiunutului
        self.__response_topic_id = np.uint8(8)  # identificator topi raspuns
        self.__response_topic = None  # topicul de raspuns
        self.__correlation_data_id = np.uint8(9)  # identificator date de corelare
        self.__correlation = None  # datele de corelare
        self.__user_property_payload_id = np.uint8(38)  # identificator proprietati utilizator
        self.__user_property_payload = None  # proprietatiile utilizatorului
        self.__will_topic_payload = None  # topicul will
        self.__will_payload = None  # continutul topicului will
        self.__username = None  # numele utilizatorului
        self.__password = None  # parola de conectare

    def calculate_variable_header_length(self):
        """Calculăm lungimea totală a câmpurilor din variable_header (excluzând câmpurile din super)"""
        length = 0

        # Adăugăm lungimea fiecărui câmp dacă nu este None
        if self.__byte is not None:
            length += 2  # np.uint16 ocupă 2 octeți
        if self.__name is not None:
            length += len(self.__name)  # lungimea numelui protocolului
        if self.__protocol_version is not None:
            length += 1  # np.uint8 ocupă 1 octet
        if self.__flags is not None:
            length += 1  # np.uint ocupă 1 octet (presupunând np.uint e echivalent cu np.uint8)
        if self.__keep_alive is not None:
            length += 2  # np.uint16 ocupă 2 octeți

        # Elemente de proprietate
        if self.__property_length is None:
            self.__property_length = FixedHeader.encode_variable_byte_integer(self.property_length())
            length += len(self.__property_length)  # lungimea nr care descrie proprietatile
        if self.__session_expiry_interval is not None:
            length += 4  # np.uint32 ocupă 4 octeți
        if self.__maximum_receive is not None:
            length += 2  # np.uint16 ocupă 2 octeți
        if self.__packet_maximum_size is not None:
            length += 4  # np.uint32 ocupă 4 octeți
        if self.__topic_alias_maximum is not None:
            length += 2  # np.uint16 ocupă 2 octeți
        if self.__request_response_information is not None:
            length += 1  # np.uint8 ocupă 1 octet
        if self.__request_problem_information is not None:
            length += 1  # np.uint8 ocupă 1 octet
        if self.__user_property is not None:
            length += len(self.__user_property[0] + self.__user_property[1]) + 4
            # lungimea proprietății utilizatorului
        if self.__authentication_method is not None:
            length += len(self.__authentication_method) + 2  # lungimea metodei de autentificare
        if self.__authentication_data is not None:
            length += len(self.__authentication_data) + 2 # lungimea datelor de autentificare

        return length

    def calculate_payload_length(self):
        """Calculez lungimea payload-ului"""
        length = 0
        if self.__client_id is not None:
            length += len(self.__client_id)  # lungimea ID-ului clientului
        if self.__will_property_length is not None:
            length += 2  # np.uint16 ocupă 2 octeți
        if self.__will_delay_interval is not None:
            length += 4  # np.uint32 ocupă 4 octeți
        if self.__payload_format_indicator is not None:
            length += 1  # np.uint8 ocupă 1 octet
        if self.__message_expiring_interval is not None:
            length += 4  # np.uint32 ocupă 4 octeți
        if self.__content_type is not None:
            length += len(self.__content_type) + 2  # lungimea tipului de conținut
        if self.__response_topic is not None:
            length += len(self.__response_topic) + 2  # lungimea topicului de răspuns
        if self.__correlation is not None:
            length += len(self.__correlation) + 2  # lungimea datelor de corelare
        if self.__user_property_payload is not None:
            length += len(self.__user_property_payload[0] + self.__user_property_payload) + 4
            # lungimea proprietății utilizatorului în payload
        if self.__will_topic_payload is not None:
            length += len(self.__will_topic_payload) + 2  # lungimea topicului will
        if self.__will_payload is not None:
            length += len(self.__will_payload) + 2  # lungimea payload-ului will
        if self.__username is not None:
            length += len(self.__username) + 2  # lungimea numelui de utilizator
        if self.__password is not None:
            length += len(self.__password) + 2  # lungimea parolei
        return length

    def property_length(self):
        length = 0

        if self.__session_expiry_interval is not None:
            length += 4  # np.uint32 ocupă 4 octeți
        if self.__maximum_receive is not None:
            length += 2  # np.uint16 ocupă 2 octeți
        if self.__packet_maximum_size is not None:
            length += 4  # np.uint32 ocupă 4 octeți
        if self.__topic_alias_maximum is not None:
            length += 2  # np.uint16 ocupă 2 octeți
        if self.__request_response_information is not None:
            length += 1  # np.uint8 ocupă 1 octet
        if self.__request_problem_information is not None:
            length += 1  # np.uint8 ocupă 1 octet
        if self.__user_property is not None:
            length += len(self.__user_property[0] + self.__user_property[0]) + 4
            # lungimea proprietății utilizatorului
        if self.__authentication_method is not None:
            length += len(self.__authentication_method) + 2  # lungimea metodei de autentificare
        if self.__authentication_data is not None:
            length += len(self.__authentication_data) + 2  # lungimea datelor de autentificare

        return length

    def encode(self) -> str:
        """ Construim un șir de caractere pentru toate câmpurile care nu sunt None """
        result = ""
        lg = self.calculate_variable_header_length() + self.calculate_payload_length()
        if lg < 256:
            self.length = FixedHeader.encode_variable_byte_integer(lg + 2)
        elif lg < 65536:
            self.length = FixedHeader.encode_variable_byte_integer(lg + 3)
        elif lg < 16777216:
            self.length = FixedHeader.encode_variable_byte_integer(lg + 4)
        else:
            self.length = FixedHeader.encode_variable_byte_integer(lg + 5)
        # pt broker facut de Emi si Alin
        # self.length = FixedHeader.encode_variable_byte_integer(lg)
        # Adăugăm primele câmpuri din pachet (presupunem că `self.type` este deja un byte)
        result += chr(self.type)  # Adăugăm `self.type` ca un singur caracter
        result += self.length.decode()  # `self.length` este deja un bytearray, îl decodificăm
        result += ''.join(chr(byte) for byte in np.uint16(4).byteswap().tobytes())
        result += self.__name
        result += ''.join(chr(byte) for byte in self.__protocol_version.byteswap().tobytes())
        result += ''.join(chr(byte) for byte in self.__flags.byteswap().tobytes())
        result += ''.join(chr(byte) for byte in np.uint16(self.__keep_alive).byteswap().tobytes())
        # result += struct.pack('!H', self.__keep_alive)
        result += self.__property_length.decode()  # `self.__property_length` este un bytearray

        # Verificăm și adăugăm câmpurile cu valori
        if self.__session_expiry_interval is not None:
            result += chr(self.__session_expiry_interval_id)
            result += ''.join(chr(byte) for byte in self.__session_expiry_interval.byteswap().tobytes())  # Folosim latin1 pentru a păstra fiecare octet ca ASCII

        if self.__maximum_receive is not None:
            result += chr(self.__maximum_receive_id)
            result += ''.join(chr(byte) for byte in self.__maximum_receive.byteswap().tobytes())  # Folosim latin1 pentru a păstra fiecare octet ca ASCII

        if self.__packet_maximum_size is not None:
            result += chr(self.__packet_maximum_size_id)
            result += ''.join(chr(byte) for byte in self.__packet_maximum_size.byteswap().tobytes())  # Folosim latin1 pentru a păstra fiecare octet ca ASCII

        if self.__topic_alias_maximum is not None:
            result += chr(self.__topic_alias_maximum_id)
            result += ''.join(chr(byte) for byte in self.__topic_alias_maximum.byteswap().tobytes()) # Folosim latin1 pentru a păstra fiecare octet ca ASCII

        if self.__request_response_information is not None:
            result += chr(self.__request_response_information_id)
            result += chr(self.__request_response_information)

        if self.__request_problem_information is not None:
            result += chr(self.__request_problem_information_id)
            result += chr(self.__request_problem_information)

        if self.__user_property is not None:
            result += chr(self.__user_property_id)
            result += ''.join(chr(byte) for byte in len(self.__user_property[0]).to_bytes(2, byteorder='big')) # Folosim
            # latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__user_property[0]
            result += ''.join(chr(byte) for byte in len(self.__user_property[1]).to_bytes(2, byteorder='big')) # Folosim
            # latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__user_property[1]

        if self.__authentication_method is not None:
            result += chr(self.__authentication_method_id)
            result += ''.join(chr(byte) for byte in len(self.__authentication_method).to_bytes(2, byteorder='big'))   #
            # Folosim latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__authentication_method

        if self.__authentication_data is not None:
            result += chr(self.__authentication_data_id)
            result += ''.join(chr(byte) for byte in self.__authentication_data.byteswap().tobytes())  # Folosim latin1
            # pentru a păstra fiecare octet ca ASCII

        if self.__client_id is not None:
            result += ''.join(chr(byte) for byte in len(self.__client_id).to_bytes(2, byteorder='big'))# Folosim latin1
            # pentru a păstra fiecare octet ca ASCII
            result += self.__client_id

        if self.__will_property_length is not None:
            result += chr(self.__will_property_length)

        if self.__will_delay_interval is not None:
            result += chr(self.__will_delay_interval_id)
            result += ''.join(chr(byte) for byte in self.__will_delay_interval.to_bytes(4, byteorder='big'))
            # Folosim latin1 pentru a păstra fiecare octet ca ASCII

        if self.__payload_format_indicator is not None:
            result += chr(self.__payload_format_indicator_id)
            result += chr(self.__payload_format_indicator)

        if self.__message_expiring_interval is not None:
            result += chr(self.__message_expiring_interval_id)
            result += ''.join(chr(byte) for byte in self.__message_expiring_interval.to_bytes(4, byteorder='big')) #
            # Folosim latin1 pentru a păstra fiecare octet ca ASCII

        if self.__content_type is not None:
            result += chr(self.__content_type_id)
            result += ''.join(chr(byte) for byte in len(self.__content_type).to_bytes(2, byteorder='big'))  # Folosim
            # latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__content_type

        if self.__response_topic is not None:
            result += chr(self.__response_topic_id)
            result += ''.join(chr(byte) for byte in len(self.__response_topic).to_bytes(2, byteorder='big')) # Folosim
            # latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__response_topic

        if self.__correlation is not None:
            result += chr(self.__correlation_data_id)
            result += ''.join(chr(byte) for byte in self.__correlation.byteswap().tobytes()) # Folosim latin1 pentru
            # a păstra fiecare octet ca ASCII

        if self.__user_property_payload is not None:
            result += chr(self.__user_property_payload_id)
            result += ''.join(chr(byte) for byte in len(self.__user_property_payload).to_bytes(2, byteorder='big'))
            # Folosim latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__user_property_payload

        if self.__will_topic_payload is not None:
            result += ''.join(chr(byte) for byte in len(self.__will_topic_payload).to_bytes(2, byteorder='big'))
            # Folosim latin1 pentru a păstra fiecare octet ca ASCII
            result += self.__will_topic_payload

        if self.__will_payload is not None:
            result += ''.join(chr(byte) for byte in self.__will_payload.byteswap().tobytes())  # Folosim latin1
            # pentru a păstra fiecare octet ca ASCII

        if self.__username is not None:
            result += ''.join(chr(byte) for byte in len(self.__username).to_bytes(2, byteorder='big'))  # Folosim latin1
            # pentru a păstra fiecare octet ca ASCII
            result += self.__username

        if self.__password is not None:
            result += ''.join(chr(byte) for byte in len(self.__password).to_bytes(2, byteorder='big'))  # Folosim latin1
            # pentru a păstra fiecare octet ca ASCII
            result += self.__password

        return result  # Returnăm șirul final

    def decode(self, packet) -> str:
        return "It is not send by the server to clinet"

    # Getter și setter pentru __property_length
    def get_property_length(self):
        return self.__property_length

    def set_property_length(self, value):
        self.__property_length = value

    # Getter și setter pentru __session_expiry_interval
    def get_session_expiry_interval(self):
        return self.__session_expiry_interval

    def set_session_expiry_interval(self, value):
        self.__session_expiry_interval = value

    # Getter și setter pentru __maximum_receive
    def get_maximum_receive(self):
        return self.__maximum_receive

    def set_maximum_receive(self, value):
        self.__maximum_receive = value

    # Getter și setter pentru __packet_maximum_size
    def get_packet_maximum_size(self):
        return self.__packet_maximum_size

    def set_packet_maximum_size(self, value):
        self.__packet_maximum_size = value

    # Getter și setter pentru __topic_alias_maximum
    def get_topic_alias_maximum(self):
        return self.__topic_alias_maximum

    def set_topic_alias_maximum(self, value):
        self.__topic_alias_maximum = value

    # Getter și setter pentru __request_response_information
    def get_request_response_information(self):
        return self.__request_response_information

    def set_request_response_information(self, value):
        self.__request_response_information = value

    # Getter și setter pentru __request_problem_information
    def get_request_problem_information(self):
        return self.__request_problem_information

    def set_request_problem_information(self, value):
        self.__request_problem_information = value

    # Getter și setter pentru __user_property
    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, value):
        self.__user_property = value

    # Getter și setter pentru __authentication_method
    def get_authentication_method(self):
        return self.__authentication_method

    def set_authentication_method(self, value):
        self.__authentication_method = value

    # Getter și setter pentru __authentication_data
    def get_authentication_data(self):
        return self.__authentication_data

    def set_authentication_data(self, value):
        self.__authentication_data = value

    # Getter și setter pentru __client_id
    def get_client_id(self):
        return self.__client_id

    def set_client_id(self, value):
        self.__client_id = value

    # Getter și setter pentru __will_property_length
    def get_will_property_length(self):
        return self.__will_property_length

    def set_will_property_length(self, value):
        self.__will_property_length = value

    # Getter și setter pentru __will_delay_interval
    def get_will_delay_interval(self):
        return self.__will_delay_interval

    def set_will_delay_interval(self, value):
        self.__will_delay_interval = value

    # Getter și setter pentru __payload_format_indicator
    def get_payload_format_indicator(self):
        return self.__payload_format_indicator

    def set_payload_format_indicator(self, value):
        self.__payload_format_indicator = value

    # Getter și setter pentru __message_expiring_interval
    def get_message_expiring_interval(self):
        return self.__message_expiring_interval

    def set_message_expiring_interval(self, value):
        self.__message_expiring_interval = value

    # Getter și setter pentru __content_type
    def get_content_type(self):
        return self.__content_type

    def set_content_type(self, value):
        self.__content_type = value

    # Getter și setter pentru __response_topic
    def get_response_topic(self):
        return self.__response_topic

    def set_response_topic(self, value):
        self.__response_topic = value

    # Getter și setter pentru __correlation
    def get_correlation(self):
        return self.__correlation

    def set_correlation(self, value):
        self.__correlation = value

    # Getter și setter pentru __user_property_payload
    def get_user_property_payload(self):
        return self.__user_property_payload

    def set_user_property_payload(self, value):
        self.__user_property_payload = value

    # Getter și setter pentru __will_topic_payload
    def get_will_topic_payload(self):
        return self.__will_topic_payload

    def set_will_topic_payload(self, value):
        self.__will_topic_payload = value

    # Getter și setter pentru __will_payload
    def get_will_payload(self):
        return self.__will_payload

    def set_will_payload(self, value):
        self.__will_payload = value

    # Getter și setter pentru __username
    def get_username(self):
        return self.__username

    def set_username(self, value):
        self.__username = value

    # Getter și setter pentru __password
    def get_password(self):
        return self.__password

    def set_password(self, value):
        self.__password = value