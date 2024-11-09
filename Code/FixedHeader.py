class FixedHeader:
    def __init__(self):
        """Initializeaza un obiect de tip FixedHeader
        Atributele include tipul pachetului si """
        self.type = None
        self.length = None

    @staticmethod
    def encode_variable_byte_integer(value) -> bytearray:
        """Encode an integer as a Variable Byte Integer as defined in MQTT v5
        Răspuns:
            bytearray: Reprezentarea codificată"""
        if value < 0 or value > 268435455:  # Valoarea trebuie să fie între 0 și 268,435,455
            raise ValueError("Value out of range for Variable Byte Integer.")

        encoded_bytes = bytearray()
        while True:
            byte = value % 128  # Extrage ultimii 7 biți
            value //= 128
            if value > 0:
                byte |= 0x80  # Setați bitul de continuare la 1 dacă urmează mai mulți octeți
            encoded_bytes.append(byte)
            if value == 0:
                break

        return encoded_bytes

    @staticmethod
    def decode_variable_byte_integer(encoded_data: bytearray) -> (int, int):
        """Decodează un Variable Byte Integer dintr-un bytearray
        Răspuns:
            (int, int): Valoarea decodificată și numărul de octeți citiți"""
        value = 0
        multiplier = 1
        bytes_read = 0

        for byte in encoded_data:
            value += (byte & 127) * multiplier  # Extrage 7 biți de date
            bytes_read += 1

            if multiplier > 128 * 128 * 128:  # Verifică dacă se depășește limita
                raise ValueError("Malformed Variable Byte Integer.")

            if (byte & 128) == 0:  # Dacă bitul de continuare este 0, am terminat
                break

            multiplier *= 128

        return value, bytes_read
