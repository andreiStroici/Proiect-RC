# $$\color{lime}DONE$$
OS: Windows
Platformă: VSCode
Etape următoare:
1. Descrierea cerințelor
    - Configurare adresa broker
    - Configurare ID client
        - Reținere timestamp pt ultima acțiune făcută
        - Reținere valoare keep alive
        - Verificare interval de timp
    - Configurare mesaj Last Will
        - Mesaj deconectare fără trimiterea pachetului DISCONNECT
2. Modalitate obținere informații stație client
3. Keep Alive client + server
4. Autentificare
5. Improvments
6. Compus din: pentru fiecare pachet modificare
7. Fisiere de logging
8. Diagrame de secvente
   - CONNECT + CONNACK + DISCONNECT -> 2.06
   - SUBSCRIBE + SUBACK/ UNSUBSCRUBE + UNSUBACK -> 2.10 Mecanismul de abonare
   - PINGREQ + PINGRESP ->2.07
   - PUBLISH + PUBACK + PUBREC + PUBREL + PUBCOMP -> 1.03