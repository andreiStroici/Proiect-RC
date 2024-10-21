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
# $$\color{red}TO$$ $$\color{red}DO$$
1. Diagrame de adaugat:
    - Autentificare cu user și parolă (+ AUTH package ca îmbunătățiri de care am putea ține cont): https://sequencediagram.org/index.html#initialData=C4S2BsFMAIEEFdgAtIDtQGMCGoD2roB3MJaeAZ0gCdUsBbGLVAE2gActzzDcrmAofhyqYQHdNADC4EGmBCsIkBjFNg0AEJVcAa2qDho8eoDK8AEbkMVEOf39ps9AFoAfFt3UAXJIDyAOX8AUUkAFUFHOQAeZw89Ki8EZDllHBB8aAAlSABHeEhyeUiXd214xMQUdFS8AmzyNnxKBxlo2LLvP0DYSQBpfjjqGLNLa1tOgOCwgY6qNxGrGzsEpKrMNIzsvIL5Qaphi0XxlcqU7FqsgsbUZr35w7Hln0me-uLgNz2vABEASRMulNwnsDqMlt4-gDJiFQkA
    - (Un)Subscribe: https://sequencediagram.org/index.html#initialData=C4S2BsFMAIAoFUB2BKAzgVwEaoMYCcRMREBzaAKHIAcBDPUHEWxYaAYXBEheroaZotoAITwB7ANaQ8veiEbNWAZSy4CmaZXKjJ0gDwBaFdnyFpALiXxhStgCUAksICi28VLwGAfMbVm8ltYAgmwA0uQcXCzeOh7mAArWADIOSgAScAB02chuuniGvqYaAfAAclY29k6usdLeReoW5ZUhoUA
    - Pingreq + Pingresp: https://sequencediagram.org/index.html#initialData=C4S2BsFMAIAUEkByBxAUKgDgQwE6gMYjYB2w0AwuCJKZrgUVqdAEI4D2A1pDuqjgCN2AD2jsAbjwpUawADRsuPAFzl2AV1IhiAc2gBpSJAwBBKpOhYAZsCmQs+ABbQAEvbwt7wVJWqkAtAB8itw4yggoAEoAogCK6L6yADz+ISoRyDEAyrCoQA
2. Sequence diagram pt threads
3. Diagrama clase
4. Funcționalitate clase
5. Interfața cu utilizatorul
6. Legătura cu soket-ul
