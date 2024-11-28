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
        self.__last_packet_id = None

    def encode(self) -> str:
        return "This packet is not send by client to broker"

    def decode(self, packet) -> str:
        if self.type != packet[0]:
            return "Malformed packet"
        i = 1
        lg = 1
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
            lg = lg + 1
        self.length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[1:i+1])
        if len(packet) - nr_bytes - 1 != self.length:
            return "Malformed packet"
        i = i + lg
        self.__packet_identifier = packet[i:i+2]
        number = np.frombuffer(self.__packet_identifier, dtype=np.uint16).byteswap()[0]
        if number != self.__last_packet_id:
            return "Malformed packet -> packet identifier doesn't match"
        i = i + 2
        j = i
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
        self.__property_length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[j:i+1])
        lg = self.__property_length
        print(len(packet))
        if lg >= len(packet) - i - 1:
            return "Malformed packet -> property length"
        if self.__property_length != 0:
            i = i + 1
            maximum = i + self.length
            while i < maximum:
                code = np.uint8(packet[i])
                match code:
                    case 31:
                        if self.__reason_string is None:
                            i = i + 1
                            number = np.frombuffer(packet[i:i+2], dtype=np.uint16).byteswap()[0]
                            i = i + 2
                            self.__reason_string = packet[i:i+number].decode()
                        else:
                            return "Malformed packet -> 2 times reason string"
                    case 38:
                        if self.__user_property is None:
                            i = i + 1
                            number = np.frombuffer(packet[i:i + 2], dtype=np.uint16).byteswap()[0]
                            i = i + 2
                            usrpp1 = packet[i:i + number].decode()
                            i = i + number
                            number = np.frombuffer(packet[i:i + 2], dtype=np.uint16).byteswap()[0]
                            i = i + 2
                            usrpp2 = packet[i:i + number].decode()
                            self.__user_property = (usrpp1, usrpp2)
                        else:
                            return "Malformed packet -> 2 times user property"
        for j in range(0, len(self.__topic_filters)):
            code = packet[i + j]
            match code:
                case 0x00:
                    print(f"UNSUBSCRIBE: Success for {self.__topic_filters}")
                case 0x11:
                    print(f"UNSUBSCRIBE: No subscription existed for {self.__topic_filters}")
                case 0x80:
                    print(f"UNSUBSCRIBE: Unspecified error for {self.__topic_filters}")
                case 0x83:
                    print(f"UNSUBSCRIBE: Implementation specific error for {self.__topic_filters}")
                case 0x87:
                    print(f"UNSUBSCRIBE: Not authorized for {self.__topic_filters}")
                case 0x8F:
                    print(f"UNSUBSCRIBE: Topic Filter invalid for {self.__topic_filters}")
                case 0x91:
                    print(f"UNSUBSCRIBE: Packet Identifier in use for {self.__topic_filters}")

        return "SUCCESS"

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

    def set_last_packet_id(self, pack_id):
        self.__last_packet_id = pack_id
