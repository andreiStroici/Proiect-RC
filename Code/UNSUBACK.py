from Code.Packet import Packet
from Code.FixedHeader import FixedHeader
from abc import ABC
import numpy as np


class UNSUBACK(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = np.uint8(176)
        self.length = None
        self.__packet_identifier = None
        self.__property_length = None
        self.__reason_string_id = np.uint8(31)
        self.__reason_string = None
        self.__user_property_id = np.uint8(38)
        self.__user_property = None
        self.__reasons_code = None
        self.__topic_filters = None

    def encode(self) -> str:
        return "This packet is not send by client to broker"

    def decode(self, packet) -> str:
        pass

    # Getter și setter pentru `__packet_identifier`
    def get_packet_identifier(self):
        return self.__packet_identifier

    def set_packet_identifier(self, value):
        self.__packet_identifier = value

    # Getter și setter pentru `__property_length`
    def get_property_length(self):
        return self.__property_length

    def set_property_length(self, value):
        self.__property_length = value

    # Getter și setter pentru `__reason_string`
    def get_reason_string(self):
        return self.__reason_string

    def set_reason_string(self, value):
        self.__reason_string = value

    # Getter și setter pentru `__user_property`
    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, value):
        self.__user_property = value

    # Getter și setter pentru `__reasons_code`
    def get_reasons_code(self):
        return self.__reasons_code

    def set_reasons_code(self, value):
        self.__reasons_code = value

    def set_topic_filters(self, topic: list):
        self.__topic_filters = topic
