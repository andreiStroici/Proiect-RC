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
        if self.type != int(packet[0]):
            return "Malformed packet -> wrong type"

        i = 1
        while packet[i] & 0b10000000: # determin lungimea pachetului
            i = i + 1

        self.length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[1:i+1])
        if self.length != len(packet) - 1 - i:
            return "Malformed packet -> wrong length"

        i = i + 1
        self.__reason_code = int(packet[i])
        match self.__reason_code:
            case 0:
                print("Normal disconnection")
            case 4:
                print("Disconnect with Will message")
            case 128:
                print("Unspecified error")
            case 129:
                print("Malformed Packet")
            case 130:
                print("Protocol Error")
            case 131:
                print("Implementation specific error")
            case 135:
                print("Not authorized")
            case 137:
                print("Server busy")
            case 139:
                print("Server shutting down")
            case 141:
                print("Keep Alive timeout")
            case 142:
                print("Session taken over")
            case 143:
                print("Topic Filter invalid")
            case 144:
                print("Topic Name invalid")
            case 147:
                print("Receive Maximum excedeed")
            case 148:
                print("Topic Alias invalid")
            case 149:
                print("Packet too large")
            case 150:
                print("Message rate too high")
            case 151:
                print("Quota excedeed")
            case 152:
                print("Administrative action")
            case 153:
                print("Payload format invalid")
            case 154:
                print("Retain not supported")
            case 155:
                print("QoS not supported")
            case 156:
                print("Use another server")
            case 157:
                print("Server moved")
            case 158:
                print("Shared Subcriptions not supported")
            case 159:
                print("Connection rate excedeed")
            case 160:
                print("Maximum connect time")
            case 161:
                print("Subscription Identifiers not supported")
            case 162:
                print("Wildcard Subscriptions not supported")

        i = i + 1
        j = i
        while packet[i] & 0b10000000: # determin lungimea antetului variabil
            i = i + 1

        self.__property_length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[j:i+1])
        if self.__property_length != len(packet) - i - 1:
            return "Malformed packet -> property length"

        i = i + 1
        if self.__property_length != 0:
            maximum = len(packet)
            while i < maximum:
                code = packet[i]
                match code:
                    case 17: # session expiry interval
                        i = i + 1
                        if self.__session_expiring_interval is None: # ma asigur ca nu e introdus de doua ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__session_expiring_interval = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Malformed packet"
                    case 31: # reason string
                        i = i + 1
                        if self.__reason_string is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+2]
                            i = i + 2
                            self.__reason_string = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Malformed packet"
                    case 38: # user property
                        i = i + 1
                        if self.__user_property is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+2]
                            i = i + 2
                            user_property1 = str(packet[i:i+length])
                            i = i + length
                            length = packet[i:i+2]
                            user_property2 = str(packet[i:i+length])
                            i = i + length
                            self.__user_property = (user_property1, user_property2)
                        else:
                            return "Malformed packet"
                    case 28: # server reference
                        i = i + 1
                        if self.__server_reference is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+2]
                            i = i + 2
                            self.__server_reference = packet[i:i+length]
                        else:
                            return "Malformed packet"
                    case _:
                        return "Malformed packet -> wrong property identifier"
        return "SUCCESS"


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
