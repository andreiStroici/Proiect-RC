# Client MQTT v5. Aplicație demonstrativă.
## Aspecte teoretice
### MQTT este o prescurtare de la Message Queuing Telemetry Transport. Acesta este un protocol de mesagerie ușor, folosit în cadrul IoT (Internet of Things) pentru aplicații cu resurse limitate. În cadrul acestui protocol comunicațiile sunt de tip publish-subsrcibe, unde un client trimite un mesaj la un server, numit broker, și alți clienți, care se abonează la anumite topicuri pentru a primi mesaje. Sevența "v5" indică versiunea protocolului.
### În cadrul documentației voi face referire la anumite tipuri de dată specifice acestui protocol. Unul dintre aceste tipuri de date este Variable Byte Integer. Acesta este un tip de date care se poate reprezenta pe un număr variabil de octeți (între 1 și 4 octeți). Fiecare octet are următoarea structură: cel mai semnificativ bit indică dacă urmează un octet (1 în caz afirmativ, 0 în caz contrar), iar următorii 7 biți constituie numărul efectiv. Un alt tip de dată specific acestui protocol, care va fi utilizat este UTF-8 Encoded String. Acesta este un șir de caractere care are caracterul codificat în [UTF8](https://www.rfc-editor.org/info/rfc3629).
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
---
### 1. Pachetul CONNECT
#### După ce s-a realizat conețiunea de rețea dintre client și broker, acesta este primul pachet trimis de client către server. Pachetul CONNECT poate fi trimis o singură dată, iar dacă în cadrul acestui proces va apărea o eroare, brokerul va închide conețiunea de rețea. Structura acestui pachet este:
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
        - **Solicitare informații despre erori**: 1 octet (0 sau 1).
        - **Proprietățile utilizatorului**: 1 octet (care este idetificatorul proprietății utilizatorului) și o pereche de șiriuri de caractere codificate cu UTF-8.
        - **Metoda de autetificare**: 1 octet (identificatorul metodei de autetificare) și urmat de un șir de caractere codificat folosind UTF-8.
        - **Datele de autentificare**: 1 octet (idetificatorul datelor de autentificare) urmat de un Binary Data (care conține datele de autentificare).
3. **Payload** 
    - **Identificatorul clientului**: șir de caractere
    - **Proprietăți Will**: compus din
        - **Lungimea proprietății**: Variable Integer Byte.
        - **Interval de întârziere pentru Will**: compus din:
            - **Idetificatorul intervalului de întârziere pentru Will**: 1 octet
            - **Durata intervalului**: întreg memorat pe 4 octeți.
        - **Identificatorul de format al Payload**: compus din:
            - **Identificator pentru formatul Payload-ului**: 1 octet.
            - **Valoarea formatului**: un octet.
        - **Durata de expirare a mesajului**: compus din:
            - **Identificator pentru durata de expirare a intervalului**: 1 octet.
            - **Valoarea intervalului**: un întreg memorat pe 4 octeți.
        - **Tipul conținutului**: compus din:
            - **Identificator pentru tipul conținutului**: 1 octet.
            - **Conținutul mesajului Will**: un șir de caractere.
        - **Topicul de răspuns**: compus din:
            - **Identificatorul topicului**: 1 octet.
            - **VȘir de caractere utilizat pentru topicul de răspuns**: un șir de caractere.
        - **Datele de corelare**: compus din:
            - **Identificator pentru datele de corelare**: 1 octet.
            - **Valoarea formatului**: Binary Data.
        - **Proprietatea utilizatorului**: compus din:
            - **Identificator pentru proprietatea utilizatorului**: 1 octet.
            - **Proprietatea**: Binary Data.
        - **Topicul Will**:  șir de caractere.
        - **Will Payload**: Binary Data.
        - **Numele utilizatorului**: șir de caractere.
        - **Parolă**: Binary Data.
---
### 2. Pachetul CONNACK
#### Pachetul CONNACK este trimis de broker ca răspuns la un pachet CONNECT. Acesta confirmă dacă conexiunea a fost acceptată și include informații despre starea conexiunii. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (0010 0000).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Acknowledge Flags**: 1 octet.
        - Biții 7-1: Rezervați și au toți valoarea 0.
        - Bit 0: Session Present (indică dacă o sesiune anterioară există).
    - **Return Code**: 1 octet (starea conexiunii).
        - 0: Conexiune acceptată.
        - 1: Refuzată - inexistentă.
        - Alte coduri pentru diferite erori.
    - **Proprietățile pachetului CONNACK**: compuse din
        - **Lungimea proprietății**: Variable Byte Integer.
        - **Durata de expirare a sesiunii**: compus din:
            - **Identificator al intervalului de expirare a sesiunii**: 1 octet.
            - **Valoarea intervalului**: întreg pe 4 octeți.
        - **Maxim de primire**: compus din: 
            - **Identificatorul maximului de primire**: 1 octet.
            - **Valoarea acestui maxim**: întreg pe 2 octeți.
        - **Maxim QoS**: compus din
            - **Identificatorul maximului QoS**: 1 octet.
            - **Valoarea maximă a QoS**: întreg pe 1 octet.
        - **Posibilitate de păstrare**: compus din:
            - **Identificatorul pentru acest câmp**: 1 octet.
            - **Valoarea care arată dacă server-ul poate păstra mesaje**: Byte.
        - **Dimensiunea maximă a pachetului**: compus din:
            - **Identificatorul dimensiunii maxime**: 1 octet.
            - **Dimensiunea maximă a pachetului**: întreg pe 4 octeți.
        - **Idetificatorul atribuit clientului**: compus din:
            - **Identificatorul acestui atribut**: 1 octet.
            - **Valoarea identificatorului atribuit clientului**: șir de caractere.
        - **Topic ALias Maxim**: compus din:
            - **Identificatorul Topic Alias Maxim**: 1 octet.
            - **DValoarea Topic Alias Maxim**: întreg pe 2 octeți.
        - **Reason String**: compus din:
            - **Identificatorul Reason String**: 1 octet.
            - **Valoarea Reason String asociat răspunsului**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identificatorul proprietăților utilizatorului**: 1 octet.
            - **Informații suplimentare**: șir de caractere.
        - **Aboanre cu wildcard disponibilă**: compus din:
            - **Identificatorul disponibiltății abonării cu wildcard**: 1 octet.
            - **Valoare care perimte această opțiune**: Byte.
        - **Identificatori pentru subsripțile disponibile**: compuis din:
            - **Identificatorul această proprietate**: 1 octet.
            - **Valoare care îmi spune dacă sunt disponibili identificatorii subscripțiilor**: Byte.
        - **Disponibilitate subscripții partajate**: compus din:
            - **Identificatorul aceste proprietăți**: 1 octet.
            - **Valoare care îmi spune dacă server-ul perimite subscripții partajate**: Byte.
        - **Informații de răspuns**: compus din:
            - **Identificatorul informațiilor de răspuns**: 1 octet.
            - **Valoare care este utilizată pentru topicul de răspuns**:șir de caractere.
        - **Referința server-ului**: compus din:
            - **Identificatorul referinței server-ului**: 1 octet.
            - **DValoare cu care clientul poate identifica alt server**: șir de caractere.
        - **Metoda de autentificare**: compus din:
            - **Identificatorul metodei de autentificare**: 1 octet.
            - **Numele metodei de autentificare**: șir de caractere.
        - **Datele de autentificare**: compus din:
            - **Identificatorul datelor de autentificare**: 1 octet.
            - **Datele de autentificare**: Byte.
3. **Acest pachet nu are payload**
---

### 3. Pachetul PUBLISH
#### Pachetul PUBLISH este utilizat de client pentru a trimite mesaje către broker. Mesajele pot avea diferite niveluri de QoS.Structura pachetului este:

1. **Antetul fix**
    - **Tip**: alcătuit din:
        - **Biții 7-4**:  au valoarea 0011.
        - **Bitul 3**: DUP Flag.
        - **Biții 2-1**: nivelul QoS.
        - **Bitul 0**: Retain
    - **Lungimea**: Variable Byte Integer (lungimea antetului variabil + payload).

2. **Antetul variabil**
    - **Topic Name**: String (subiectul mesajului).
    - **Packet Identifier**: 2 octeți (pentru QoS 1 și QoS 2).
    - **Properties**: Câmp opțional care poate conține informații suplimentare. Acestea sunt:
        - **Lungimea pachetului**: Variable Byte Integer.
        - **Formatul Payload-ului**: compus din:
            - **Identificatorul formatului payload-ului**: 1 octet.
            - **Tipul formatului**: Byte.
        - **Intervalul de timp pentru expirarea mesajului**: compus din:
            - **Indentificator**: Byte.
            - **Valoarea intervalului**: număr întreg pe 4 octeți.
        - **Topic Alias**:
            : compus din:
            - **Identificator**: 1 octet.
            - **Valoarea topicului alias**: întreg pe 4 octeți.
        - **Topicul de răspuns**: compus din:
            : compus din:
            - **Identificatorul topicului de răspuns**: 1 octet.
            - **Numele topicului de rapsuns**: șir de caractere.
        - **Date de corelare**: compus din:
            : compus din:
            - **Identificatorul datelor de corelare**: 1 octet.
            - **Valoare**: Binary.
        - **Proprietățile utilizatorului**: compus din:
            - **Identificatorul proprietățile utilizatorului**: 1 octet.
            - **Propeietățile utilzatorului**: pereche de șiruri de caractere.
        - **Identificatorul subscripției**: compus din:
            - **Identificator**: 1 octet.
            - **Identificatorul subscripției**: Variable Byte Integer.
        - **Tipul conținutului**: compus din:
            - **Identificatorul tipului conținutului**: 1 octet.
            - **Descrierea conținutului**: șir de caractere.

3. **Payload**: Conținutul efectiv al mesajului.

---

### 4. Pachetul PUBACK (QoS 1)
#### Pachetul PUBACK este trimis de broker ca răspuns la un mesaj PUBLISH cu QoS 1. Acesta confirmă primirea mesajului. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (0100 0000).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).
    - **PUBACK REASON CODE**: 1 octet
    - **Proprietăți**: aceste sunt un câmp opțional. Acestea sunt:
        - **Lungime**: Variable Byte Integer. 
        - **Reason String**: compus din:
            - **Identificator**: 1 octet.
            - **Motivul asociat cu acest răspuns**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.
3. **Acest pachet nu are Payload**

---

### 5. Pachetul PUBREC (QoS 2)
#### Pachetul PUBREC este trimis de broker ca răspuns la un mesaj PUBLISH cu QoS 2, confirmând primirea acestuia.Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (0101 0000).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).
    - **Proprietăți**: aceste sunt un câmp opțional. Acestea sunt:
        - **Lungime**: Variable Byte Integer. 
        - **Reason String**: compus din:
            - **Identificator**: 1 octet.
            - **Motivul asociat cu acest răspuns**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.
3. **Acest pachet nu are Payload**

---

## 6. Pachetul PUBREL (QoS 2)
#### Pachetul PUBREL este trimis de client pentru a confirma că a primit pachetul PUBREC. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (0110 0010).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).
        - **Proprietăți**: aceste sunt un câmp opțional. Acestea sunt:
        - **Lungime**: Variable Byte Integer. 
        - **Reason String**: compus din:
            - **Identificator**: 1 octet.
            - **Motivul asociat cu acest răspuns**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.

3. **Acest pachet nu are Payload.**
---

### 7. Pachetul PUBCOMP (QoS 2)
#### Pachetul PUBCOMP este trimis de broker pentru a confirma finalizarea procesului QoS 2. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (0111 0000).
    - **Lungimea**: 1 octet (2).

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul mesajului confirmat).
     - **Proprietăți**: aceste sunt un câmp opțional. Acestea sunt:
        - **Lungime**: Variable Byte Integer. 
        - **Reason String**: compus din:
            - **Identificator**: 1 octet.
            - **Motivul asociat cu acest răspuns**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.
---

### 8. Pachetul SUBSCRIBE
#### Pachetul SUBSCRIBE este trimis de client pentru a se abona la un subiect. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (1000 0010).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul abonării).
    - **Proprietăți**: compuse din:
        - **Lungime**: Variable Byte Integer.
        - **Identificatorul subscripției**: compus din:
            - **Identificatorul proprietății**: 1 octet.
            - **Identificartorul subsrcipțieie**: Variable Byte Integer.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.

3. **Payload**
    - **Topic Filters**: compus din:
        - **Lungime**: întreg pe 2 octeți
        - **Topic Filters efectiv**: String (subiectul la care se abonează clientul).
    - **Opțiunile subscripției**: 1 octet alcătuit astfel:
        - **Biții 7-6**: rezevați și au valoarea 0.
        - **Biții 5-4**: Retain Handling.
        - **Bitul 3**: Retain as Published.
        - **Bitul 2**: No Local.
        - **Biții 1-0**: QoS.

---
### 9. SUBACK
#### Pachetul acesta este trimis de la server pentru confirmarea procesării cerieri de abonare. Acesta are următoarea structură:
1. **Antetul fix**
    - **Tip-ul pachetului**: 1 octet (10010000).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Identificatorul pachetului**: este identic cu identificatorul trimis de pachetul SUBSCRIBE.
    - **Proprietăți**
        - **Lungime**: Variable Byte Integer.
        - **Reason String**: compus din:
            - **Identificator**: 1 octet.
            - **Motivul asociat cu acest răspuns**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.
3. **Payload**  
Acesta conține o listă de Rason Code care corespund fiecărui Topic Filter din pachetul SUBSCRIBE.

---

### 10. Pachetul UNSUBSCRIBE
#### Pachetul UNSUBSCRIBE este trimis de client pentru a renunța la o abonare existentă. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (1010 0010).
    - **Lungimea**: Variable Byte Integer.

2. **Antetul variabil**
    - **Packet Identifier**: 2 octeți (identificatorul anulării).
    - **Proprietăți**
        - **Lungimea proprietăților**: Variable Byte Integer.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.

3. **Payload**
    - **Topic Filters**: 
        - **Lungime Topic Filters**: 2 octeți
        - **Topicurile efective**: String (subiectul de la care se renunță).

---
### 11. UNSUBACK
#### Acesta este pachetul trimis de server către client pentru a confirma primirea pachetului de UNSUBACK. Structura acestuia este:
1. **Antentul fix**
    - **Tipul pachetului**: 1 octet (10110000).
    - **Lungime a antetului variabil și a payload-ului**: Variable Byte Ineger.

2. **Antetul variabil**
    - **Identifiacatorul pachetului**: 2 octeți.
    - **Prorpietăți**
        - **Lungime**: Variable Byte Integer.
        - **Reason String**: compus din:
            - **Identificator**: 1 octet.
            - **Motivul asociat cu acest răspuns**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.

3. **Payload**  
Acesta conține o listă de Rason Code care corespund fiecărui Topic Filter din pachetul UNSUBSCRIBE.

---

### 12. Pachetul PINGREQ
#### Pachetul PINGREQ este trimis de client pentru a verifica dacă brokerul este încă conectat. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (1100 0000).
    - **Lungimea**: 0 (nu are antet variabil sau payload).
2. **Nu există antet variabil**
3. **Nu exitsă Payload**
---

### 13. Pachetul PINGRESP

### Descriere
#### Pachetul PINGRESP este trimis de broker ca răspuns la PINGREQ, confirmând că brokerul este activ. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (1101 0000).
    - **Lungimea**: 0 (nu are antet variabil sau payload).

---

### 14. Pachetul DISCONNECT
#### Pachetul DISCONNECT este trimis de client pentru a închide conexiunea cu brokerul. Structura pachetului este:

1. **Antetul fix**
    - **Tip**: 1 octet (1110 0000).
    - **Lungimea**: 0 (nu are antet variabil sau payload).
2. **Antetul variabil**
    - **Motivul deconectării**: Byte.
    - **Proprietăți**
        - **Lungime**: Variable Byte Integer
        - **Durata de expirarea a sesiunii**: compusă din:
            - **Identificatorul duratei de expirare**:  Byte.
            - **Valoarea duratei de timp**: număr întreg pe 4 octeți.
        - **Reason String**: compus din:
            - **Identificator**: Byte
            - **Motivul pentru deconectare**: șir de caractere.
        - **Proprietățile utilizatorului**: compus din:
            - **Identifcator al proprietăților utilizatorului**: 1 octet.
            - **Proprietățile utilizatorului**: șir de caractere.
        - **Referință server**: compus din:
            - **Identificatorul referinței server**: Byte.
            - **Cod pe care clientul îl folosește pentru a identifica un nou server**: șir de caractere.  
3. **Nu exitsă Payload**
---

## 15. Pachetul AUTH

### Descriere


            


