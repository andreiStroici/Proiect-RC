from abc import ABC

from Code.Packet import Packet


class PINGREQ(Packet, ABC):
    def __init__(self):
        """Se creaza obiectul care descrie pachetul PINGREQ"""
        super().__init__()
        self.type = 192

    def encode(self) -> str:
        """Vom codifica pachetul sub forma unui sir de caractrere pentru a-l
        putea trimite de la client la broker
            param: nu are niciun parametru
            ret: reutrneaza un sir de caractere care constituie pachetul care trebuie trimis"""
        ret = ""
        ret = ret + self.type.to_bytes(1, byteorder='big').decode('latin')
        ret = ret + '\0'
        return ret

    def decode(self, packet) -> str:
        return "Pingreq: This packet is not sent from broker to client"
