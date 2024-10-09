# Client MQTT v5. Aplicație demonstrativă.
## Aspecte teoretice
### MQTT este o prescurtare de la Message Queuing Telemetry Transport. Acesta este un protocol de mesagerie ușor, folosit în cadrul IoT (Internet of Things) pentru aplicații cu resurse limitate. În cadrul acestui protocol comunicațiile sunt de tip publish-subsrcibe, unde un client trimite un mesaj la un server, numit broker, și alți clienți, care se abonează la anumite topicuri pentru a primi mesaje. Sevența "v5" indică versiunea protocolului.
### În cadrul documentației voi face referire la anumite tiprui de dată specifice acestui protocol. Unul dintre aceste tipuri de date este Variable Byte Integer. Acesta este un tip de date care se poate reprezenta pe un număr variabil de octeți (între 1 și 4 octeți). Fiecare octet are următoarea structură: cel mai semnificativ bit indică dacă urmează un octet (1 în caz afirmativ, 0 în caz contrar), iar următorii 7 biți constituie numărul efectiv.
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

