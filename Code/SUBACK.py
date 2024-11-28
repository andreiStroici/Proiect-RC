from Code.FixedHeader import FixedHeader
from Code.Packet import Packet
import numpy as np
from abc import ABC


class SUBACK(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = np.uint8(144)
        self.length = None
        self.__packet_identifier = None
        self.__property_length = None
        self.__reason_string_id = np.uint8(31)
        self.__reason_string = None
        self.__user_property_id = np.uint8(38)
        self.__user_property = None
        self.__payload = None
        self.__topic_filters = []
        self.__last_packet_identifier = None

    def encode(self) -> str:
        return "This packet is send only from the broker to the client"

    def decode(self, packet) -> str:
        i = 0
        type = packet[0]
        if self.type != type:
            return "Malformed packet -> type"
        i = i + 1
        lg = 1
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
            lg = lg + 1
        self.length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[1:i + 1])
        if self.length != len(packet) - 1 - lg:
            return "Malformed packet -> packet length"
        i = i + 1
        self.__packet_identifier = packet[i:i+2]
        number = np.frombuffer(self.__packet_identifier, dtype=np.uint16).byteswap()[0]
        if number != self.__last_packet_identifier:
            return "Malformed packet -> packet_identifier"
        i = i + 2
        j = i
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
        self.__property_length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[j:i + 1])
        lg = self.__property_length
        if lg >= len(packet) - i - 1:
            return "Malformed packet -> property length"
        maximum = lg + i
        while i < maximum:
            code = packet[i]
            match code:
                case 31:  # reason string
                    i = i + 1
                    if self.__reason_string is None:
                        length = packet[i:i + 2]
                        i = i + 2
                        self.__reason_string = str(packet[i:i + length])
                        i = i + length
                    else:
                        return "Malformed packet -> 2 times reason string"
                case 38:  # user property
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
                        return "Malformed packet -> 2 times user property"
        if len(packet) - i - 1 != len(self.__topic_filters):
            return "Malformed packet -> topic length"
        for j in range(0, len(self.__topic_filters)):
            code = packet[i + j + nr_bytes]
            match code:
                case 0:
                    print(f"Granted QoS 0 for {self.__topic_filters[j]}")
                case 1:
                    print(f"Granted QoS 1 for {self.__topic_filters[j]}")
                case 2:
                    print(f"Granted QoS 2 for {self.__topic_filters[j]}")
                case 0x80:
                    print(f"Unspecified error for {self.__topic_filters[j]}")
                case 0x83:
                    print(f"Implementation specific error for {self.__topic_filters[j]}")
                case 0x87:
                    print(f"Not authorized for {self.__topic_filters[j]}")
                case 0x8F:
                    print(f"Topic Filter invalid for {self.__topic_filters[j]}")
                case 0x91:
                    print(f"Packet Identifier in use for {self.__topic_filters[j]}")
                case 0x97:
                    print(f"Quota exceeded for {self.__topic_filters[j]}")
                case 0x9E:
                    print(f"Shared Subscriptions not supported for {self.__topic_filters[j]}")
                case 0xA1:
                    print(f"Subscription Identifiers not supported for {self.__topic_filters[j]}")
                case 0xA2:
                    print(f"Wildcard Subscriptions not supported for {self.__topic_filters[j]}")
                case _:
                    return "Malformed packet"
        return "SUCCESS"

    # Getter și setter pentru __reason_string
    def get_reason_string(self):
        return self.__reason_string

    def set_reason_string(self, reason_string: str):
        self.__reason_string = reason_string

    # Getter și setter pentru __user_property
    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, user_property: tuple[str, str]):
        if len(user_property) == 2 and isinstance(user_property[0], str) and isinstance(user_property[1], str):
            self.__user_property = user_property
        else:
            raise ValueError("User property trebuie să fie un tuple cu două string-uri.")

    # Getter și setter pentru __payload
    def get_payload(self):
        return self.__payload

    def set_payload(self, payload: str):
        self.__payload = payload

    # Setter pentru __topic_filters
    def set_topic_filters(self, topic_filters: list[str]):
        self.__topic_filters = topic_filters

    def set_last_packet_identifier(self, pack_id):
        self.__last_packet_identifier = pack_id
