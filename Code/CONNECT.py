from abc import ABC

from Code.Packet import Packet


class CONNECT(Packet, ABC):
    def __init__(self):
        """Vom crea obiectul care va descrie pachetul CONNECT
        inculzand toate informatiile pachetului
        Antetul fix e mostenit"""
        super().__init__()
        self.__name = None  # numele protocolului
        self.__protocol_version = None  # verisunea protocolului
        self.__flags = None  # flag-urile folosite
        self.__keep_alive = None  # durata intervalului de keep alive
        self.__property_length = None  # lunginea proprietatiilor pachetlui
        self.__session_expiry_interval_id = None  # identifiactorul duratei de expirare a intervalului
        self.__session_expiry_interval = None  # durata de expirare a intervalului in secude
        self.__maximum_receive_id = None  # identificator pentru maxim de primire
        self.__maximum_receive = None  # valoare identificatorlului maxim de primire
        self.__packet_maximum_size_id = None  # identificatorul dimensiunii maxime a pachetului
        self.__packet_maximum_size = None  # dimensiunea maxima a dimensiunii maxime a pachetului
        self.__topic_alias_maximum_id = None  # identificatorul pentru topic alias maximum
        self.__topic_alias_maximum = None  # valoarea topic alias maximum
        self.__request_response_information_id = None  # identificator cerere pentru informații despre răspuns
        self.__request_response_information = None  # cerere pentru informații despre răspuns
        self.__request_problem_information_id = None  # identificator solicitare informații despre erori
        self.__request_problem_information = None  # solicitare informații despre erori
        self.__user_property_id = None  # identificatorul prorprietatiilor utilizatorului
        self.__user_property = None  # proprietatiile utilizatorlui
        self.__authentication_method_id = None  # identificatorul metodei de autentificare
        self.__authentication_method = None  # metoda de autentificare
        self.__authentication_data_id = None  # identifiacatorul datelor de autentificare
        self.__authentication_data = None  # datele de autentificare
        self.__client_id = None  # identificatorul clientului
        self.__will_delay_interval_id = None  # identificatorlul properietatii will
        self.__will_property_length = None  # lungimea proprietatii will
        self.__will_delay_interval_id = None  # identificator intervalului de delay will
        self.__will_delay_interval = None  # valoare intervalului de delay will in secunde
        self.__payload_format_indicator_id = None  # identificator format payload indicator
        self.__payload_format_indicator = None  # valoare fromat payload identificator
        self.__message_expiring_interval_id = None  # identificator durata expirare mesaj
        self.__message_expiring_interval = None  # valoare expirare interval in secunde
        self.__content_type_id = None  # identificator tip de contiunt
        self.__content_type = None  # tipul contiunutului
        self.__response_topic_id = None  # identificator topi raspuns
        self.__response_topic = None  # topicul de raspuns
        self.__correlation_data_id = None  # identificator date de corelare
        self.__correlation = None  # datele de corelare
        self.__user_property_payload_id = None  # identificator proprietati utilizator
        self.__user_property_payload = None  # proprietatiile utilizatorului
        self.__will_topic_payload = None  # topicul will
        self.__will_payload = None  # continutul topicului will
        self.__username = None  # numele utilizatorului
        self.__password = None  # parola de conectare

    def encode(self) -> str:
        pass

    def decode(self) -> str:
        return "It is not send by the server to clinet"
