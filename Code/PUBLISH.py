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
        self.__QoS = None
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

        return lg

    def variable_header_length(self):
        lg = 0
        if self.__topic_name is not None:
            lg += 2 + len(self.__topic_name.encode('utf-8'))
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

        # adaug lungimea mesajului (payload)
        if self.__message is not None:
            lg += len(self.__message)

        self.length = FixedHeader.encode_variable_byte_integer(lg)
        match self.__QoS:
            case 1:
                self.type += 2
            case 2:
                self.type += 4

        ret += self.type.to_bytes(1, byteorder='big').decode('latin')
        ret += self.length.decode()

        if self.__topic_name is not None:
            ret += len(self.__topic_name.encode('utf-8')).to_bytes(2, 'big').decode('latin')
            ret += self.__topic_name

        if self.__packet_identifier is not None:
            ret += self.__packet_identifier.to_bytes(2, 'big').decode('latin')

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
            ret += self.__subscription_identifier.to_bytes(1, byteorder='big').decode('latin')

        if self.__content_type is not None:
            ret += self.__content_type_id.to_bytes(1, byteorder='big').decode('latin')
            ret += len(self.__content_type.encode('utf-8')).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__content_type

        if self.__message is not None:
            # ret += len(self.__message).to_bytes(2, byteorder='big').decode('latin')
            ret += self.__message

        return ret

    def decode(self, packet) -> str:
        if int(self.type) & 0xF0 != int(packet[0]) & 0xF0:
            return "Publish: Malformed packet -> wrong type"

        self.__QoS = (int(packet[0]) & 0x06) >> 1 # pentru a extrage tipul de QoS al pachetului

        i = 1
        while packet[i] & 0b10000000: # determin lungimea pachetului
            i = i + 1

        self.length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[1:i+1])
        if self.length != len(packet) - 1 - i:
            return "Publish: Malformed packet -> wrong length"

        i = i + 1
        j = i
        while packet[i] & 0b10000000: # determin lungimea antetului variabil
            i = i + 1

        self.__property_length, nr_bytes = FixedHeader.decode_variable_byte_integer(packet[j:i+1])
        if self.__property_length > len(packet) - i - 1:
            return "Publish: Malformed packet -> property length"

        topic_name_lg = int.from_bytes(packet[i:i + 2], byteorder='big')
        i = i + 2
        self.__topic_name = packet[i:i + topic_name_lg].decode('latin')

        i = i + topic_name_lg

        if self.__QoS > 0:
            self.__packet_identifier = int.from_bytes(packet[i:i+2], byteorder='big')
            i = i + 2

        i = i + 1
        maximum = len(packet)
        if self.__property_length != 0:
            while i < maximum:
                code = packet[i]
                match code:
                    case 1: # payload format indicator
                        i = i + 1
                        if self.__payload_format is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__payload_format = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case 2: # message expiry interval
                        i = i + 1
                        if self.__message_expiry_interval is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__message_expiry_interval = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case 35: # topic alias
                        i = i + 1
                        if self.__topic_alias is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__topic_alias = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case 8: # response topic
                        i = i + 1
                        if self.__response_topic is None: # ma asigur ca e introdus de 2 ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__response_topic = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case 9: # correlation data
                        i = i + 1
                        if self.__correlation_data is None: # ma asigur ca nu am introdus de 2 ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__correlation_data = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case 38: # user property
                        i = i + 1
                        if self.__user_property is None:  # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i + 2]
                            i = i + 2
                            user_property1 = str(packet[i:i + length])
                            i = i + length
                            length = packet[i:i + 2]
                            user_property2 = str(packet[i:i + length])
                            i = i + length
                            self.__user_property = (user_property1, user_property2)
                        else:
                            return "Publish: Malformed packet"
                    case 11: # subscription identifier
                        i = i + 1
                        if self.__subscription_identifier is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+2]
                            i = i + 2
                            self.__subscription_identifier = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case 3: # content type
                        i = i + 1
                        if self.__content_type is None: # ma asigur ca nu e introdus de 2 ori
                            length = packet[i:i+1]
                            i = i + 1
                            self.__content_type = str(packet[i:i+length])
                            i = i + length
                        else:
                            return "Publish: Malformed packet"
                    case _:
                        i = i + 1
                        self.__message = packet[i:maximum].decode('latin')
                        i = maximum
        if self.__message is None and i < len(packet):
            self.__message = packet[i:maximum].decode('latin')
        return "SUCCESS"

    # Getters and Setters for all attributes
    def get_QoS(self):
        return self.__QoS

    def set_QoS(self, value):
        self.__QoS = value

    def get_topic_name(self):
        return self.__topic_name

    def set_topic_name(self, value):
        self.__topic_name = value

    def get_packet_identifier(self):
        return self.__packet_identifier

    def set_packet_identifier(self, value):
        self.__packet_identifier = value

    def get_property_length(self):
        return self.__property_length

    def set_property_length(self, value):
        self.__property_length = value

    def get_payload_format(self):
        return self.__payload_format

    def set_payload_format(self, value):
        self.__payload_format = value

    def get_message_expiry_interval(self):
        return self.__message_expiry_interval

    def set_message_expiry_interval(self, value):
        self.__message_expiry_interval = value

    def get_topic_alias(self):
        return self.__topic_alias

    def set_topic_alias(self, value):
        self.__topic_alias = value

    def get_response_topic(self):
        return self.__response_topic

    def set_response_topic(self, value):
        self.__response_topic = value

    def get_correlation_data(self):
        return self.__correlation_data

    def set_correlation_data(self, value):
        self.__correlation_data = value

    def get_user_property(self):
        return self.__user_property

    def set_user_property(self, value):
        self.__user_property = value

    def get_subscription_identifier(self):
        return self.__subscription_identifier

    def set_subscription_identifier(self, value):
        self.__subscription_identifier = value

    def get_content_type(self):
        return self.__content_type

    def set_content_type(self, value):
        self.__content_type = value

    def get_message(self):
        return self.__message

    def set_message(self, value):
        self.__message = value