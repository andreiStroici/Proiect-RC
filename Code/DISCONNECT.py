from abc import ABC

from Code.FixedHeader import FixedHeader
from Code.Packet import Packet


class DISCONNECT(Packet, ABC):
    def __init__(self):
        """Se creaza obiectul care descrie pachetul DISCONNECT"""
        super().__init__()
        self.type = 224 # 0xE0
        self.length = None
        self.__reason_code = None # codul de identificare pentru disconnect
        self.__property_length = None
        self.__session_expiring_interval_id = 17
        self.__session_expiring_interval = None
        self.__reason_string_id = 31
        self.__reason_string = None
        self.__user_property_id = 38
        self.__user_property = None
        self.__server_reference_id = 28
        self.__server_reference = None

    def variable_header_property_length(self):
        lg = 0

        # Elemente de proprietate
        if self.__session_expiring_interval is not None:
            lg += 1
            lg += 4 # intervalul e pe 4 octeti
        if self.__reason_string is not None:
            lg += 1
            lg += 2 + len(self.__reason_string)
        if self.__user_property is not None:
            lg += 1
            lg += 2 + len(self.__user_property[0])
            lg += 2 + len(self.__user_property[1])
        if self.__server_reference is not None:
            lg += 1
            lg += 2 + len(self.__server_reference)
        return lg

    def variable_header_length(self):
        lg = 1
        property_lg = self.variable_header_property_length()
        lg += len(FixedHeader.encode_variable_byte_integer(property_lg))
        lg += property_lg
        return lg


    def encode(self) -> str:
        """Vom codifica pachetul sub forma unui sir de caractrere pentru a-l
        putea trimite de la client la broker
            param: nu are niciun parametru
            ret: reutrneaza un sir de caractere care constituie pachetul care trebuie trimis"""
        ret = ""
        lg = self.variable_header_length()

        self.length = FixedHeader.encode_variable_byte_integer(lg)

        ret += self.type.to_bytes(1, byteorder='big').decode('latin')
        ret += self.length.decode()
        ret += self.__reason_code.to_bytes(1, byteorder='big').decode('latin')
        ret += FixedHeader.encode_variable_byte_integer((self.variable_header_property_length())).decode()

        if self.__session_expiring_interval is not None:
            ret += self.__session_expiring_interval_id.to_bytes(1, byteorder='big').decode('latin')
            ret += self.__session_expiring_interval.to_bytes(4, byteorder='big').decode('latin')

        if self.__reason_string is not None:
            ret += self.__reason_string_id.to_bytes(1, byteorder ='big').decode('latin')
            ret += len(self.__reason_string.encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__reason_string

        if self.__user_property is not None:
            ret += self.__user_property_id.to_bytes(1, byteorder= 'big').decode('latin')
            ret += len(self.__user_property[0].encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__user_property[0]
            ret += len(self.__user_property[1].encode('utf-8')).to_bytes(2, byteorder= 'big').decode('latin')
            ret += self.__user_property[1]

        if self.__server_reference is not None:
            ret += self.__server_reference_id.to_bytes(1, byteorder='big').decode('latin')
            ret += len(self.__server_reference.encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__server_reference

        return ret

    def decode(self, packet) -> str:
        return "This packet is not sent from broker to client"

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
