class FixedHeader:
    def __init__(self):
        """Initializeaza un obiect de tip FixedHeader
        Atributele include tipul pachetului si """
        self.type = None
        self.length = None

    @staticmethod
    def encode_variable_byte_integer(value) -> bytearray:
        """Conversie int to reprezentarea binara
        Raspuns:
            bytearray: care va constitui valoarea codificata"""
        data_bytes = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
        length = len(data_bytes)

        if length > 65535:  # Ma asigur ca nu depasesc dimensiunea maxima
            raise ValueError("Data length exceeds maximum allowed size for MQTT binary data.")

        length_bytes = length.to_bytes(2, byteorder='big')

        return length_bytes + data_bytes
