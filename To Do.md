# $$\color{red}TO$$ $$\color{red}DO$$
1. Cozi de mesaje vs pipe.
2. QoS la nivel de pachet SUBSCRIBE în momentul trimiterii unui pachet PUBLISH cu un anumit Qos => adăugare atribut suplimentar la Client.
3. Atribut timer la Client => pentru mecanismul Keep Alive.
4. Scoatem thread-ul Send  ✅   
[noua diagramă](https://sequencediagram.org/index.html#initialData=C4S2BsFMAIBUAsBOkCGATaBnSBHArpAHYDGMaIKA5oigLYBQ9ADioqMSC4cNLSiIWjAkqNM1btOKbtGLgQRHsOTpxbEBy49kpEADcYLYgGtIwTEJGqW6zdJ7ZCGI6fOWVY+nwHvRAWgA+OQUZZVEALmIVYEhMRmDFX3RAnUh9QxQTMwsw9Ejo2PoE0Ks0QMdnTNcc0vCK3kxKaGbmgF4Als7mqNQYuOKlUoAeP1T06BdspLRwsYN6NFjgRAB7AE8sIkqst1yxb0E9kYHpuq3oNBRgFCL5RL2UyF0DCaqpvfDF4hXCQieedpdTrGEDgcALJarDZzDI7GoeLz8Q7DPwnD5fH5-YjARE+B5BO4lDzhEFgiGYZbrWSEwYeIA)
5. Socket pe windows ?? 
Nu merge pooling-ul in W....  
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

<!--- 
$$\color{grey}Andrei$$
$$\color{green}Denisa$$
✅ marchează că acea parte a fost scrisă și urmează să fie verificată
--->
