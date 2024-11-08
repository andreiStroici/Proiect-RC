from Code.Packet import Packet
from abc import ABC
import numpy as np
from Code.FixedHeader import FixedHeader


class CONNACK(Packet, ABC):
    def __init__(self):
        super().__init__()
        super().type = np.uint8(32) # tipul pachetului
        super().length = None
        self.connack_flags = np.uint8(0)
        self.reason_code = None  # codul care il intoarce server-ul
        self.property_length = None  # lungimea antetului variabil
        self.session_expiry_interval_id = np.uint8(17)  # identificatorlui duratei intervalului de expirare a sesiunii
        self.session_expiry_interval = None  # durata intervalului de expirare a sesiunii in secude
        self.__maximum_receive_id = np.uint8(33)  # identificator pentru maxim de primire
        self.__maximum_receive = None  # valoare identificatorlului maxim de primire
        self.max_qos_id = np.uint8(36)  # identificatorul pentru QoS maxim
        self.max_qos = None  # valoarea maxima a QoS
        self.retain_available_id = np.uint8(37)  # idetificator maxim de primire
        self.retain_available = None  # valoare maxim de primire
        self.__packet_maximum_size_id = np.uint8(39)  # identificatorul dimensiunii maxime a pachetului
        self.__packet_maximum_size = None  # dimensiunea maxima a dimensiunii maxime a pachetului
        self.__assigned_client_id_id = np.uint8(18)  # identificator pentru id client dat de server
        self.__assigned_client_id = None  # id-ul de client dat de broker
        self.__topic_alias_maximum_id = np.uint8(34)  # identificatorul pentru topic alias maximum
        self.__topic_alias_maximum = None  # valoarea topic alias maximum
        self.__user_property_id = np.uint8(38)  # identificatorul prorprietatiilor utilizatorului
        self.__user_property = None  # proprietatiile utilizatorlui
        self.__wildcard_subscription_available_id = np.uint8(40)
        self.__wildcard_subscription_available = None
        self.__subscription_identifiers_id = np.uint8(42)
        self.__subscription_identifiers = None
        self.__server_keep_alive_id = np.uint8(19)
        self.__server_keep_alive = None
        self.__response_information_id = np.uint8(26)
        self.__response_information = None
        self.__server_reference_id = np.uint8(28)
        self.__server_reference = None
        self.__authentication_method_id = np.uint8(21)
        self.__authentication_method = None
        self.__authentication_data_id = np.uint8(22)
        self.__authentication_data = None

    def encode(self) -> str:
        return "This packet is not send by the client"

    def decode(self, packet) -> str:
        self.type = packet[0]
        return "SUCCESS"

    # Getter și Setter pentru reason_code
    def get_reason_code(self):
        return self.reason_code

    def set_reason_code(self, value):
        self.reason_code = value

    # Getter și Setter pentru property_length
    def get_property_length(self):
        return self.property_length

    def set_property_length(self, value):
        self.property_length = value

    # Getter și Setter pentru session_expiry_interval
    def get_session_expiry_interval(self):
        return self.session_expiry_interval

    def set_session_expiry_interval(self, value):
        self.session_expiry_interval = value

    # Getter și Setter pentru __maximum_receive
    def get_maximum_receive(self):
        return self.__maximum_receive

    def set_maximum_receive(self, value):
        self.__maximum_receive = value

    # Getter și Setter pentru max_qos
    def get_max_qos(self):
        return self.max_qos

    def set_max_qos(self, value):
        self.max_qos = value

    # Getter și Setter pentru retain_available
    def get_retain_available(self):
        return self.retain_available

    def set_retain_available(self, value):
        self.retain_available = value

    # Getter și Setter pentru __packet_maximum_size
    def get_packet_maximum_size(self):
        return self.__packet_maximum_size

    def set_packet_maximum_size(self, value):
        self.__packet_maximum_size = value

    # Getter și Setter pentru __assigned_client_id
    def get_assigned_client_id(self):
        return self.__assigned_client_id

    def set_assigned_client_id(self, value):
        self.__assigned_client_id = value

    # Getter și Setter pentru __topic_alias_maximum
    def get_topic_alias_maximum(self):
        return self.__topic_alias_maximum

    def set_topic_alias_maximum(self, value):
        self.__topic_alias_maximum = value

    # Getter și Setter pentru __user_property
    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, value):
        self.__user_property = value

    # Getter și Setter pentru __wildcard_subscription_available
    def get_wildcard_subscription_available(self):
        return self.__wildcard_subscription_available

    def set_wildcard_subscription_available(self, value):
        self.__wildcard_subscription_available = value

    # Getter și Setter pentru __subscription_identifiers
    def get_subscription_identifiers(self):
        return self.__subscription_identifiers

    def set_subscription_identifiers(self, value):
        self.__subscription_identifiers = value

    # Getter și Setter pentru __server_keep_alive
    def get_server_keep_alive(self):
        return self.__server_keep_alive

    def set_server_keep_alive(self, value):
        self.__server_keep_alive = value

    # Getter și Setter pentru __response_information
    def get_response_information(self):
        return self.__response_information

    def set_response_information(self, value):
        self.__response_information = value

    # Getter și Setter pentru __server_reference
    def get_server_reference(self):
        return self.__server_reference

    def set_server_reference(self, value):
        self.__server_reference = value

    # Getter și Setter pentru __authentication_method
    def get_authentication_method(self):
        return self.__authentication_method

    def set_authentication_method(self, value):
        self.__authentication_method = value

    # Getter și Setter pentru __authentication_data
    def get_authentication_data(self):
        return self.__authentication_data

    def set_authentication_data(self, value):
        self.__authentication_data = value
