# $$\color{red}TO$$ $$\color{red}DO$$
1. Cozi de mesaje vs pipe.
2. QoS la nivel de pachet SUBSCRIBE în momentul trimiterii unui pachet PUBLISH cu un anumit Qos => adăugare atribut suplimentar la Client.
3. Atribut timer la Client => pentru mecanismul Keep Alive.
4. Socket pe windows ??
Nu merge pooling-ul in W....  :(
 Vin cu o propunere noua de cod:

```Python
import socket

# Creare socket de conexiune
s_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_conn.connect(('server_ip_address', port_number))

try:
    while True:
        # Așteptare blocantă pentru primirea mesajului
        data = s_conn.recv(dim_pachet)  # Aici nu există un timeout
        if data:
            print("Pachet primit:", data)
            # Aici poți adăuga procesarea specifică pachetului MQTT
        else:
            print("Conexiune închisă de server.")
            break  # Ieșire din buclă la deconectare
finally:
    # Închidere socket la final
    s_conn.close()

```
5. Functii pentru interfete (plus completare disable campuri optionale = topic text) -> $$\color{green}Denisa$$
6. Functionalitate pachete CONNECT si CONNACK si eventual pt celelate pachete scheletul 
7. EXCEPTII: a. Tratare exceptie cand programul este inchis din compilator si nu din interfata (BaseException)
8. Schimbare (schema) interfata pentru Subscribe (putem alege QoS) -> $$\color{green}Denisa$$
9. Importarea codului din alte fisiere
<!--- 
$$\color{grey}Andrei$$
$$\color{green}Denisa$$
✅ marchează că acea parte a fost scrisă și urmează să fie verificată
--->
