from abc import ABC
import numpy as np
from Code.Packet import Packet


class SUBSCRIBE(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = np.uint8(0x82)
        self.length = None
        self.__packet_identifier = np.uint16(0x000A)
        self.__property_length = None
        self.__subscription_id_id = np.uint8(11)
        self.__subscription_id = None
        self.__user_property_id = np.uint8(38)
        self.__user_property = None
        self.__subscription_options = None
        self.__topic_filters_lengths = []
        self.__topic_filters = []

    def variable_header_length(self) -> int:
        """Aceasta functie va calculca lungimea antetului variabil
        ea va returna un numar intreg reprezentand aceasta lungime"""
        lg = 2
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

    def encode(self) -> str:
        result = ""
        return result

    def decode(self, packet) -> str:
        return "Packet subscribe is not send by broker to client"
