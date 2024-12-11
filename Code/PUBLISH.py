from abc import ABC
from sys import byteorder

from Code.FixedHeader import FixedHeader
from Code.Packet import Packet


class PUBLISH(Packet, ABC):
    def __init__(self):
        """Se creaza obiectul care descrie pachetul PUBLISH"""
        super().__init__()
        self.type = 48 # 0x30
        self.length = None
        self.__reason_code = None  # codul de identificare pentru publish
        self.__topic_name = None
        self.__packet_identifier = None
        self.__property_length = None
        self.__payload_format_id = 1
        self.__payload_format = None
        self.__message_expiry_interval_id = 2
        self.__message_expiry_interval = None
        self.__topic_alias_id = 35
        self.__topic_alias = None
        self.__response_topic_id = 8
        self.__response_topic = None
        self.__correlation_data_id = 9
        self.__correlation_data = None
        self.__user_property_id = 38
        self.__user_property = None
        self.__subscription_identifier_id = 11
        self.__subscription_identifier = None
        self.__content_type_id = 3
        self.__content_type = None
        self.__message = None

    def variable_header_property_length(self):
        lg = 0

        # Elemente de proprietate
        if self.__payload_format is not None:
            lg += 1
            lg += 1
        if self.__message_expiry_interval is not None:
            lg += 1
            lg += 4
        if self.__topic_alias is not None:
            lg += 1
            lg += 2
        if self.__response_topic is not None:
            lg += 1
            lg += len(self.__response_topic)
        if self.__correlation_data is not None:
            lg += 2
        if self.__user_property is not None:
            lg += 2 + len(self.__user_property[0])
            lg += 2 + len(self.__user_property[1])
        if self.__subscription_identifier is not None:
            lg += 2
        if self.__content_type is not None:
            lg += 1
            lg += len(self.__content_type)
        if self.__message is not None:
            lg += len(self.__message)

        return lg

    def variable_header_length(self):
        lg = 1
        if self.__topic_name is not None:
            lg += len(self.__topic_name)
        if self.__packet_identifier is not None:
            lg += 2 # ocupa 2 octeti

        property_lg = self.variable_header_property_length()
        lg += len(FixedHeader.encode_variable_byte_integer(property_lg))
        lg += property_lg

        return lg


    def encode(self) -> str:
        """Vom codifica pachetul sub forma unui sir de caractrere pentru a-l
        putea trimite de la client la broker
            param: nu are niciun parametru
            ret: returneaza un sir de caractere care constituie pachetul care trebuie trimis"""
        ret = ""

        lg = self.variable_header_length()

        self.length = FixedHeader.encode_variable_byte_integer()
        ret += self.length.decode()
        ret += self.__reason_code.to_bytes(1, byteorder='big').decode('latin')
        ret += FixedHeader.encode_variable_byte_integer((self.variable_header_property_length())).decode()

        if self.__payload_format is not None:
            ret += self.__payload_format_id.to_bytes(1, byteorder='big').decode('latin')
            ret += self.__payload_format.to_bytes(1, byteorder='big').decode('latin')

        if self.__message_expiry_interval is not None:
            ret += self.__message_expiry_interval_id.to_bytes(1, byteorder='big').decode('latin')
            ret += self.__message_expiry_interval.to_bytes(4, byteorder='big').decode('latin')

        if self.__topic_alias is not None:
            ret += self.__topic_alias_id.to_bytes(1, byteorder='big').decode('latin')
            ret += self.__topic_alias.to_bytes(2, byteorder='big').decode('latin')

        if self.__response_topic is not None:
            ret += self.__response_topic_id.to_bytes(1, byteorder='big').decode('latin')
            ret += len(self.__response_topic.encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')

        if self.__correlation_data is not None:
            ret += self.__correlation_data_id.to_bytes(1, byteorder='big').decode('latin')
            ret += self.__correlation_data.to_bytes(1, byteorder='big').decode('latin')

        if self.__user_property is not None:
            ret += self.__user_property_id.to_bytes(1, byteorder='big').decode('latin')
            ret += len(self.__user_property[0].encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__user_property[0]
            ret += len(self.__user_property[1].encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__user_property[1]

        if self.__subscription_identifier is not None:
            ret += self.__subscription_identifier_id.to_bytes(2, byteorder='big').decode('latin')

        if self.__content_type is not None:
            ret += self.__content_type_id.to_bytes(1, byteorder='big').decode('latin')
            ret += len(self.__content_type.encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__content_type

        if self.__message is not None:
            ret += self.__message

        return ret

    def decode(self, packet) -> str:

        return ""

    def get_reason_code(self):
        return self.__reason_code

    def set_reason_code(self, value):
        self.__reason_code = value

    def get_property_length(self):
        return self.__property_length

    def set_property_length(self, value):
        self.__property_length = value

    def get_session_expiring_interval(self):
        return self.__session_expiring_interval

    def set_session_expiring_interval(self, value):
        self.__session_expiring_interval = value

    def get_reason_string(self):
        return self.__reason_string

    def set_reason_string(self, value):
        self.__reason_string = value

    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, value):
        self.__user_property = value

    def get_server_reference(self):
        return self.__server_reference

    def set_server_reference(self, value):
        self.__server_reference = value
