from abc import ABC
from Code.Packet import Packet
from Code.FixedHeader import FixedHeader


class SUBSCRIBE(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = 130
        self.length = None
        self.__packet_identifier = 0x000A
        self.__property_length = None
        self.__subscription_id_id = 11
        self.__subscription_id = None
        self.__user_property_id = 38
        self.__user_property = None
        self.__subscription_options = None
        self.__topic_filters_lengths = []
        self.__topic_filters = []

    def variable_header_length(self) -> int:
        """Aceasta functie va calculca lungimea antetului variabil
        ea va returna un numar intreg reprezentand aceasta lungime"""
        local = self.variable_header_property_length()
        lg = 2 + local + len(FixedHeader.encode_variable_byte_integer(local))
        return lg

    def variable_header_property_length(self):
        """Functia determina lungimea prorpietatilor din varable header
                nu arre parametrii
                returneaza un itnreg care reprezint a lungimea """
        lg = 0
        if self.__subscription_id is not None:
            # daca am continut in subscription identifier
            # il adaug la lungime
            lg = lg + len(self.__subscription_id) + 1
        if self.__user_property is not None:
            # daca acest pachet are proprietatile utilizatorului
            # atunci le adaug si pe aceastea la lungime
            # plus 5 pt ca am 4 octeti (cate 2 pt lugimea sirului) si inca unul pt id
            lg = lg + len(self.__user_property[0] + self.__user_property[1]) + 5
        return lg

    def payload_length(self):
        """Determin lungimea payload-ului
            nu are parametrii
            returneaza un intreg care indica lungimea payload-ului"""
        lg = 2 * len(self.__topic_filters_lengths)  # cu aceasta voi calcula lungimea payload-ului pachetului
        # valoarea initiala este egala cu suma tuturor octetiilor care descriu lungimea fiecarui topic
        for  topic in self.__topic_filters:
            lg = lg + len(topic)
        return lg

    def encode(self) -> str:
        result = ""
        self.length = FixedHeader.encode_variable_byte_integer(
            self.variable_header_length() +
            self.payload_length() + 1
        )
        result = result + self.type.to_bytes(1, byteorder='big').decode('latin')
        result = result + self.length.decode()
        result = result + self.__packet_identifier.to_bytes(2, byteorder='big').decode('latin')
        result = (result +
                  FixedHeader.encode_variable_byte_integer(self.variable_header_property_length()).decode())
        if self.__subscription_id is not None:
            result = result + self.__subscription_id_id.to_bytes(1, byteorder='big').decode('latin')
            result = result + self.__subscription_id.decode()
        if self.__user_property is not None:
            result = result + self.__user_property_id.to_bytes(1, byteorder='big').decode('latin')
            # result = result + "".join(chr(byte) for byte in
            #                           np.uint16(len(self.__user_property[0])).byteswap().to_bytes(2, byteorder="big"))
            result = result + len(self.__user_property[0]).to_bytes(2, byteorder='big').decode('latin')
            result = result + self.__user_property[1]
            # result = result + "".join(chr(byte) for byte in
            #                           np.uint16(len(self.__user_property[1])).byteswap().to_bytes(2, byteorder="big"))
            result = result + len(self.__user_property[1]).to_bytes(2, byteorder='big').decode('latin')
            result = result + self.__user_property[1]
        for i in range(0, len(self.__topic_filters)):
            result = result + len(self.__topic_filters[i]).to_bytes(2,byteorder='big').decode('latin')
            result = result + self.__topic_filters[i]
        result = result + chr(self.__subscription_options)
        return result

    def decode(self, packet) -> str:
        return "Packet subscribe is not send by broker to client"

    # Getter and Setter methods
    def set_subscription_id(self, subscription_id: str):
        self.__subscription_id = subscription_id

    def get_subscription_id(self):
        return self.__subscription_id

    def set_user_property(self, user_property: tuple):
        self.__user_property = user_property

    def get_user_property(self):
        return self.__user_property

    def set_subscription_options(self, options):
        self.__subscription_options = options

    def get_subscription_options(self):
        return self.__subscription_options

    def set_topic_filters(self, topic_filters: list):
        self.__topic_filters = self.__topic_filters + topic_filters
        self.__topic_filters_lengths = self.__topic_filters_lengths + [len(topic_filters)]

    def get_topic_filters(self):
        return self.__topic_filters

    def set_packet_identifier(self, identifier):
        self.__packet_identifier = identifier

    def get_packet_identifier(self):
        return self.__packet_identifier
