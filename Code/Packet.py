from abc import ABC, abstractmethod

from Code.FixedHeader import FixedHeader


class Packet(ABC, FixedHeader):
    @abstractmethod
    def encode(self) -> str:
        """Codifica continutul pachetului intr-un string
        Raspuns:
            str: un sir de caractere care constiutuie contiunutul pachetului codificat"""
        pass

    @abstractmethod
    def decode(self) -> str:
        """Decodifica contiunutul unui pachet
            Raspuns:
                str: care va indica daca pachetul este sau nu malformat"""
        pass
