# Client MQTT v5. Aplicație demonstrativă.
## Aspecte teoretice
### MQTT este o prescurtare de la Message Queuing Telemetry Transport. Acesta este un protocol de mesagerie ușor, folosit în cadrul IoT (Internet of Things) pentru aplicații cu resurse limitate. În cadrul acestui protocol comunicațiile sunt de tip publish-subsrcibe, unde un client trimite un mesaj la un server, numit broker, și alți clienți, care se abonează la anumite topicuri pentru a primi mesaje. Sevența "v5" indică versiunea protocolului.
### În cadrul documentației voi face referire la anumite tiprui de dată specifice acestui protocol. Unul dintre aceste tipuri de date este Variable Byte Integer. Acesta este un tip de date care se poate reprezenta pe un număr variabil de octeți (între 1 și 4 octeți). Fiecare octet are următoarea structură: cel mai semnificativ bit indică dacă urmează un octet (1 în caz afirmativ, 0 în caz contrar), iar următorii 7 biți constituie numărul efectiv. Un alt tip de dată specific acestui protocol, care va fi utilizat este UTF-8 Encoded String. Acesta este un șir de caractere care are caracterul codificat în [UTF8](https://www.rfc-editor.org/info/rfc3629).
### Un client este un program sau un dispozitiv care folosește protocolul de comunicație MQTT. Un client poate realiza următoarele acțiuni: 
### 1. Deschide o conețiune cu serverul.
### 2. Publică mesaje, de care alți clienți pot fi interesați.
### 3. Se abonează la topicurile de care este interesat.
### 4. Se dezabonează de la topicurile care nu îl mai interesează.
### 5. Închide conexiunea cu server-ul.
### Pentru a se putea realiza comunicarea între clineți, dar și între client și server se folosesc pachete, numite pachete de control.  Fiecare pahet are o structură specifică compusă din: antet fix, antet variabil și conținutul efectiv al mesajului. 
#### 1. Antetul fix
#### Acesasta este prezent la toate pachetele. Primul octet din acesta are următoarea structură: biții 7-4 reprezintă tipul pachetului (sunt valori cuprinse între 1 și 15), iar biții 3-0 reprezintă flag-urile specifice fiecărui pachet. Următorii octeți sunt pentru a indica nummărul de octeți rămași din pachet (cei care compun antetul variabil și conținutul mesajului). Lungimea mesajului este dată de numărul de octeți, iar această valoare este meomorată în formatul dat de tipul Variable Byte Integer.
#### 2. Antetul Variabil
#### Acesta poate lipsi din structura pachetului. Acesta se află între antetul fix și conținutul propriu-zis al mesajului. Conținutul acestui antet va depinde de tipul pachetului, însă sunt apar și elemente comune, cum ar fi: identificatorul pachetului, propietățiile (care sunt compuse la rândul lor din 2 componente: lungimea zonei unde sunt proprietățiile și proprietățiile efective). Acest câmp poate apărea pentru pachetele de tipul PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP, SUBSCRIBE, SUBACK, UNSUBSCRIBE, UNSUBACK.
#### 3. Conținutul mesajului
#### Acesta este partea finală a unui pachet. Acesta este necesar pentru pachetele de tip: CONNECT, SUBSCRIBE; SUBACK, UNSUBSCRIBE, UNSUBACK și opțional pentru PUBLISH.
### Înainte de a începe clasificarea pachetelor trebuie să definim încă un termen: calitatea serviciului (QoS = Quality of Service). Acesta definește nivelul de garanție a livrăririi mesajului și este folosit pentru pachetele de tip  PUBLISH. Acesta este codificat pe doi biți și are următoarele valori:
#### 1. Qos 0  (cel mult o dată)
#### Acesta este cel mai simplu și rapid Qos, dar în același timp este și cel mai puțin fiabil. Pentru acest QoS, clientul trimite un mesaj la broker, iar acesta din urmă încearcă să îl livreze la abonați, fără a trimite o confirmare.
#### 2. QoS 1  (cel puțin o dată)
#### Pentru acest tip de QoS este garantat că pachetul va ajunge la destinatar. Clientul sau broker-ul trebuie sa trimită o confirmare pentru fiecare mesaj. Fluxul de mesaje are următoarea structură:
    1. PUBLISH -> Clientul trimite mesajul către broker.
    2. PUBACK -> broker-ul confirmă primirea mesajului print trimiterea acestui pachet.
    3. Retransmiterea -> Dacă după un anumit interval de timp nu s-a primit confirmarea primirii mesajului, clientul îl va retrimite.
#### 3. QoS 2 (exact o dată)
#### Deși este cel mai complex QoS, acesta este și cel mai fiabil.  Acesta asigură faptul că mesajul a fost publicat o singură dată. Fluxul de mesaj al acestui QoS este:
    1. PUBLISH -> clientul trimite mesajul către broker.
    2. PUBREC -> broker-ul a primit mesajul și va trimite o confirmare.
    3. PUBREL -> clientul trimite acest pachet pentru a confirma primirea mesajului de confirmare parțială.
    4. PUBCOMP -> se semnalează că mesajul a fost livrat și procesat o singură dată.
### În cadrul procesului de comunicație se utilizează diferite pachete: CONNECT, CONACK, PUBLISH, PUBACK, PUBREC, PUBREL, PUBCOMP, SUBSCRIBE, SUBACK, UNSUBSCRIBE, UNSUBACK, PINREQ, PINGRESP, DISCONNECT. În cele ce umrează vom face o scurtă prezentarer a fiecărui pachet.
### 1. Pachetul CONNECT
#### După ce s-a realizat conețiunea de rețea dintre client și broler, acesta este primul pachet trimis de client către server. Pachetul CONNECT poate fi trimis o singură dată, iar dacă în cadrul acestui proces va apărea o eroare, brokerul va închide conețiunea de rețea. Structura acestui pachet este:
1. **Antetul fix**
    - **Tip**: 1 octet (0001 0000).
    - **Lungimea**: Variable Byte Integer (lungimea antetului variabil + payload).

2. **Antetul variabil**
    - **Numele protocolului**:
        - 1 octet: 0x00 (indică începutul string-ului).
        - 1 octet: 0x04 (lungimea numelui protocolului).
        - 4 octeți: "MQTT" (0x4D, 0x51, 0x54, 0x54).
    - **Versiunea protocolului**: 1 octet (0x05).
    - **Flag-urile de conectare**: 1 octet.
        - Bit 7: User Name Flag.
        - Bit 6: Password Flag.
        - Bit 5: Will Retain.
        - Biții 4-3: QoS (calitatea serviciului).
        - Bit 2: Will Flag.
        - Bit 1: Clean Start.
        - Bit 0: Rezervat (0).
    - **Keep Alive**: 2 octeți (numărul de secunde pentru păstrarea conexiunii).
    - **Proprietățile conexiunii**:
        - **Lungimea proprietății**: Variable Byte Integer.
        - **Timpul de expirare al sesiunii**: 4 octeți.
        - **Maxim de primire**: 2 octeți.
        - **Dimensiunea maximă a pachetului**: 4 octeți.
        - **Topic Alias Maximum**: 2 octeți.
        - **Cerere pentru informații despre răspuns**: 1 octet (0 sau 1).
        

## 2. Pachetul CONNACK

### Descriere
Pachetul CONNACK este trimis de broker ca răspuns la un pachet CONNECT. Acesta confirmă dacă conexiunea a fost acceptată și include informații despre starea conexiunii.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (0010 0000).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Acknowledge Flags**: 1 octet.
        - Bit 7: Rezervat (0).
        - Bit 6: Session Present (indică dacă o sesiune anterioară există).
    - **Return Code**: 1 octet (starea conexiunii).
        - 0: Conexiune acceptată.
        - 1: Refuzată - inexistentă.
        - Alte coduri pentru diferite erori.

---

## 3. Pachetul PUBLISH

### Descriere
Pachetul PUBLISH este utilizat de client pentru a trimite mesaje către broker. Mesajele pot avea diferite niveluri de QoS.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (0011).
    - **Lungimea**: Variable Byte Integer (lungimea antetului variabil + payload).

2. **Antetul variabil**
    - **Topic Name**: String (subiectul mesajului).
    - **Packet Identifier**: 2 octeți (pentru QoS 1 și QoS 2).
    - **Properties**: Câmp opțional care poate conține informații suplimentare.

3. **Payload**: Conținutul efectiv al mesajului.

---

## 4. Pachetul PUBACK (QoS 1)

### Descriere
Pachetul PUBACK este trimis de broker ca răspuns la un mesaj PUBLISH cu QoS 1. Acesta confirmă primirea mesajului.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (0100 0000).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).

---

## 5. Pachetul PUBREC (QoS 2)

### Descriere
Pachetul PUBREC este trimis de broker ca răspuns la un mesaj PUBLISH cu QoS 2, confirmând primirea acestuia.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (0101 0000).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).

---

## 6. Pachetul PUBREL (QoS 2)

### Descriere
Pachetul PUBREL este trimis de client pentru a confirma că a primit pachetul PUBREC.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (0110 0010).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).

---

## 7. Pachetul PUBCOMP (QoS 2)

### Descriere
Pachetul PUBCOMP este trimis de broker pentru a confirma finalizarea procesului QoS 2.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (0111 0000).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).

---

## 8. Pachetul SUBSCRIBE

### Descriere
Pachetul SUBSCRIBE este trimis de client pentru a se abona la un subiect.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (1000 0010).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul abonării).
    - **Topic Filters**: String (subiectul la care se abonează clientul).
    - **Requested QoS**: 1 octet (nivelul QoS solicitat).

---

## 9. Pachetul UNSUBSCRIBE

### Descriere
Pachetul UNSUBSCRIBE este trimis de client pentru a renunța la o abonare existentă.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (1010 0010).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul anulării).
    - **Topic Filters**: String (subiectul de la care se renunță).

---

## 10. Pachetul DISCONNECT

### Descriere
Pachetul DISCONNECT este trimis de client pentru a închide conexiunea cu brokerul.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (1110 0000).
    - **Lungimea**: 0 (nu are antet variabil sau payload).

---

## 11. Pachetul PINGREQ

### Descriere
Pachetul PINGREQ este trimis de client pentru a verifica dacă brokerul este încă conectat.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (1100 0000).
    - **Lungimea**: 0 (nu are antet variabil sau payload).

---

## 12. Pachetul PINGRESP

### Descriere
Pachetul PINGRESP este trimis de broker ca răspuns la PINGREQ, confirmând că brokerul este activ.

### Structura pachetului

1. **Antetul fix**
    - **Tip**: 1 octet (1101 0000).
    - **Lungimea**: 0 (nu are antet variabil sau payload).

---

## 13. Pachetul AUTH

### Descriere


            


