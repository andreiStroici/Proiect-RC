from abc import ABC
import numpy as np
from Code.Packet import Packet


class PINGRESP(Packet, ABC):
    def __init__(self):
        super().__init__()
        self.type = np.uint8(208)

    def encode(self) -> str:
        return "This packet is sent only from the broker to client"

    def decode(self, packet):
        if self.type != packet[0]:
            return "Malformed packet"
        if packet[1] != 0:
            return "Malformed packet"
        return "SUCCESS"
