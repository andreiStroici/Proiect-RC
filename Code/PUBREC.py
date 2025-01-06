from Code.FixedHeader import FixedHeader
from Code.Packet import Packet
from abc import ABC


class PUBREC(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = 0x50
        self.length = None
        self.__packet_identifier = None
        self.__reason_code = None
        self.__property_length = None
        self.__reason_string_id = 31
        self.__reason_string = None
        self.__user_property_id = 38
        self.__user_property = None
        self.__last_packet_identifier = None

    def property_length(self) -> int:
        lg = 0
        if self.__reason_string is not None:
            lg = lg + 2
            lg = lg + len(self.__reason_string)

        if self.__user_property is not None:
            lg = lg + 2
            lg = lg + len(self.__reason_string)

        return lg

    def variable_header_length(self) -> int:
        lg = 0
        lg = self.property_length()
        if lg < 256:
            lg = lg + 1
        elif lg < 65536:
            lg = lg + 2
        elif lg < 16777216:
            lg = lg + 2
        else:
            lg = lg + 4
        lg = lg + 1
        lg = lg + 2
        return lg

    def encode(self) -> str:
        result = ""
        result = result + self.type.to_bytes(1, byteorder='big').decode('latin')
        result = result + FixedHeader.encode_variable_byte_integer(self.variable_header_length()).decode("latin")
        result = result + self.__packet_identifier.to_bytes(2, byteorder='big').decode('latin')
        result = result + self.__reason_code.to_bytes(1, byteorder='big').decode('latin')
        result = result + FixedHeader.encode_variable_byte_integer(self.property_length()).decode('latin')
        if self.__reason_string is not None:
            result = result + self.__reason_string_id.to_bytes(1, byteorder='big').decode('latin')
            result = result + len(self.__reason_string).to_bytes(2, byteorder='big').decode('latin')
            result = result + self.__reason_string
        if self.__user_property is not None:
            result = result + self.__user_property_id.to_bytes(1, byteorder='big').decode('latin')
            result = result + len(self.__user_property[0]).to_bytes(2, byteorder='big').decode('latin')
            result = result + self.__user_property[0]
            result = result + len(self.__user_property[1]).to_bytes(2, byteorder='big').decode('latin')
            result = result + self.__user_property[1]
        return result

    def decode(self, packet) -> (str, str):
        message_reason_code = None
        if self.type != int(packet[0]):
            return "Malformed packet -> wrong type"

        lg = len(packet)
        i = 1
        while packet[i] & 0b10000000:  # determin lungimea pachetului
            i = i + 1
        self.length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[1:i + 1])
        lg -= (1 + nr_bytes)
        if self.length != len(packet) - 1 - i:
            return "Malformed packer -> wrong length"

        i = i + 1
        self.__packet_identifier = int(packet[i]) * 256 + int(packet[i + 1])
        if self.__packet_identifier != self.__last_packet_identifier:
            return "Malformed packet -> packet identifier"

        if lg == 2:
            print("Pubrec: Success")
            message_reason_code = "Success"
            return "SUCCESS", message_reason_code

        if i < lg:
            i = i + 2
            self.__reason_code = int(packet[i])
            match self.__reason_code:
                case 0:
                    print("Pubrec: Success")
                    message_reason_code = "Success"
                case 16:
                    print("Pubrec: No matching subscribers")
                    message_reason_code = "No matching subscribers"
                case 128:
                    print("Pubrec: Unspecified error")
                    message_reason_code = "Unspecified error"
                case 131:
                    print("Pubrec: Implementation specific error")
                    message_reason_code = "Implementation specific error"
                case 135:
                    print("Pubrec: Not authorized")
                    message_reason_code = "Not authorized"
                case 144:
                    print("Pubrec: Topic Name invalid")
                    message_reason_code = "Topic Name invalid"
                case 145:
                    print("Pubrec: Packet identifier in use")
                    message_reason_code = "Packet identifier in use"
                case 151:
                    print("Pubrec: Quota exceeded")
                    message_reason_code = "Quota exceeded"
                case 153:
                    print("Pubrec: Payload format invalid")
                    message_reason_code = "Payload format invalid"

        if i < lg:
            i = i + 1
            j = i
            while packet[i] & 0b10000000:  # determin lungimea antetului variabil
                i = i + 1
            self.__property_length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[j:i + 1])
            lg -= nr_bytes
            if self.__property_length != len(packet) - i - 1:
                return "Malformed packet -> property length"

        if i < lg:
            i = i + 1
            if self.__property_length != 0:
                maximum = len(packet)
                while i < maximum:
                    code = packet[i]
                    match code:
                        case 31:  # reason string
                            i = i + 1
                            if self.__reason_string is None:  # ma asigur ca nu e introdus de 2 ori
                                length = packet[i:i + 2]
                                i = i + 2
                                self.__reason_string = str(packet[i:i + length])
                                i = i + length
                            else:
                                return "Malformed packet"
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
                        case _:
                            return "Malformed packet -> wrong property identifier"
        return "SUCCESS", message_reason_code

    # Setters and Getters for each None-initialized attribute
    def set_packet_identifier(self, packet_identifier):
        self.__packet_identifier = packet_identifier

    def get_packet_identifier(self):
        return self.__packet_identifier

    def set_reason_code(self, reason_code):
        self.__reason_code = reason_code

    def get_reason_code(self):
        return self.__reason_code

    def set_property_length(self, property_length):
        self.__property_length = property_length

    def get_property_length(self):
        return self.__property_length

    def set_reason_string(self, reason_string):
        self.__reason_string = reason_string

    def get_reason_string(self):
        return self.__reason_string

    def set_user_property(self, user_property):
        self.__user_property = user_property

    def get_user_property(self):
        return self.__user_property

    def set_last_packet_identifier(self, last_packet_identifier):
        self.__last_packet_identifier = last_packet_identifier