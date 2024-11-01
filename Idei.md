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
3. [Client interface](https://www.wut.de/e-577ww-07-apus-000.php)
4. Modalitate de conversie int to binary data
```Python
def int_to_mqtt_binary_data(value: int) -> bytes:
    # Conversie int to reprezentarea binara 
    data_bytes = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
    length = len(data_bytes)
    
    # Ma asigur ca nu depaseste lungimea impusa
    if length > 65535:
        raise ValueError("Data length exceeds maximum allowed size for MQTT binary data.")

    length_bytes = length.to_bytes(2, byteorder='big')
    
    return length_bytes + data_bytes
```
5. Client User Interface:
   - în cazul trimiterii pachetelor SUBSCRIBE/PUBLISH, să încercăm să disponibilizăm câmpul care selectează QoS-ul: dacă s-a ales pachetul SUBSCRIBE, să fie indisponibil, dacă s-a ales PUBLISH să fie disponibil)