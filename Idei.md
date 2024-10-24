# $$\color{yellow}Idei$$
1. Modialitate de codificare pt variable byte integer
```Python
def encode_variable_byte_integer(value):
    encoded_bytes = bytearray()
    while True:
        byte = value % 128
        value //= 128
        if value > 0:
            byte |= 0x80
        encoded_bytes.append(byte)
        if value == 0:
            break
    return encoded_bytes
```

2. Transmitere pachet prin socket-uri
```Python
import socket

# Creare obiect soket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectare la server folodind adresa IP si portul
s.connect(('server_ip_address', port_number))

# mqtt_packet contine datele sub forma uniui string
s.send(mqtt_packet.encode())  # codificare string in octeti

# Close the socket
s.close()

```
