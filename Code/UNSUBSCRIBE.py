from Code.FixedHeader import FixedHeader
from Code.Packet import Packet
from abc import ABC
import numpy as np


class UNSUBSCRIBE(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = np.uint8(162)
        self.length = None
        self.__packet_identifier = None
        self.__property_length = None
        self.__user_property_id = np.uint8(38)
        self.__user_property = None
        self.__topic_filter = None

    def variable_header_property_length(self):
        if self.__user_property is not None:
            return 2 + self.__user_property[0] + self.__user_property[1]
        else:
            return 0

    def variable_header_length(self):
        lg = 2 + self.variable_header_property_length()
        return lg

    def payload_length(self):
        lg = 0
        for i in self.__topic_filter:
            lg = lg + 2 + len(i)
        return lg

    def encode(self) -> str:
        result = ""
        self.length = FixedHeader.encode_variable_byte_integer(self.variable_header_length() + self.payload_length())
        result = result + chr(self.type)
        result = result + self.length.decode()
        result = result + ''.join(byte for byte in np.uint16(self.__packet_identifier).tobytes(2, byteorder='big'))
        result = result + FixedHeader.encode_variable_byte_integer(self.variable_header_property_length()).decode()
        if self.__user_property is not None:
            result = result + chr(self.__user_property_id)
            result = result + ''.join(byte for byte in
                                      np.uint16(len(self.__user_property[0])).tobytes(2, bytorder='big'))
            result = result + self.__user_property[0]
            result = result + ''.join(byte for byte in
                                      np.uint16(len(self.__user_property[1])).tobytes(2, bytorder='big'))
            result = result + self.__user_property[1]
        for topic in self.__topic_filter:
            result = result + ''.join(byte for byte in np.uint16(len(topic)).tobytes(2, bytorder='big'))
            result = result + topic
        return result

    def decode(self, packet) -> str:
        return "This packet is send by the client to the broker"

    # Getter și Setter pentru atributele None
    def get_length(self):
        return self.length

    def set_length(self, value):
        self.length = value

    def get_packet_identifier(self):
        return self.__packet_identifier

    def set_packet_identifier(self, value):
        self.__packet_identifier = value

    def get_property_length(self):
        return self.__property_length

    def set_property_length(self, value):
        self.__property_length = value

    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, value):
        self.__user_property = value

    def get_topic_filter(self):
        return self.__topic_filter

    def set_topic_filter(self, value):
        self.__topic_filter = value
