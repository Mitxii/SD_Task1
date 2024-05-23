import colorama
import threading
import uuid
import time

# Importar altres classes
from server_log import ServerLog
from name_server import name_server
import private_chat

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

# Classe per les funcions de tots els chats
class MessageBroker:
    
    # Constructor
    def __init__(self):
        # Inicialitzar logger
        self.logger = ServerLog(self)
        # Inicialitzar cues de peticions de connexió
        self.connection_requests = {}
        # Inicialitzar chats privats
        self.private_chats = {}
        
        
    # Funció per sol·licitar un chat privat
    def connect_chat(self, request):
        self.logger.log(f"{colorama.Fore.YELLOW + request.username + colorama.Fore.RESET} vol iniciar un chat privat amb {colorama.Fore.YELLOW + request.others_username + colorama.Fore.RESET}")

        # Comprovar que no es vulgui iniciar un chat amb ell mateix
        if request.username == request.others_username:
            return (False, "No pots obrir un chat amb tu mateix.")
        # Comprovar que el client existeixi (estigui connectat)
        elif not name_server.exists_client(request.others_username):
            self.logger.error(f"No s'ha trobat el client {colorama.Fore.YELLOW + request.others_username + colorama.Fore.RESET}")
            return (False, "No s'ha trobat el client.")
        else:
            # Inicialitzar cua de peticions de l'altre client i afegir l'usuari que ha fet la sol·licitud
            self.connection_requests[request.others_username] = []
            self.connection_requests[request.others_username].append((request.username, ""))
            self.logger.log(f"Afegit a la cua de {colorama.Fore.YELLOW + request.others_username + colorama.Fore.RESET} -> {self.connection_requests[request.others_username]}")

            # Bucle per esperar la resposta de l'altre client
            while True:
                time.sleep(1)

                answered = True
                # Recòrrer les peticions de l'altre client per trobar la nostra
                for connection_request in self.connection_requests[request.others_username]:
                    # Si la petició segueix i el segon valor és "", no s'ha respost encara
                    if request.username == connection_request[0] and connection_request[1] == "":
                        answered = False
                    # Si la petició segueix i el segon valor no és "", s'ha respost i aquest segon valor és l'identificador del chat
                    elif request.username == connection_request[0] and connection_request[1] != "":
                        chat_id = connection_request[1]
                        # Eliminar petició de la cua
                        self.connection_requests[request.others_username].remove(connection_request)
                        # Retornar l'identificador del chat
                        return (True, chat_id)
                
                # Si s'ha recorregut tota la llista i no s'ha trobat la nostra petició és perquè l'altre client l'ha eliminat (l'ha denegat)
                if answered: return (False, "El client no ha acceptat la petició.")
    
    
    # Funció per escoltar peticions de chat
    def listen_connections(self, request):
        while True:
            time.sleep(2)
            # Si la cua de peticions té algun client, retornar el nom d'usuari del primer
            if request.username in self.connection_requests and self.connection_requests[request.username]:
                return self.connection_requests[request.username][0][0]
            
    
    # Funció per respondre a una petició de chat
    def answer_connection(self, request):
        # Recòrrer totes les peticions de la cua
        for connection_request in self.connection_requests[request.username]:
            # Interceptar la petició que es vol respondre
            if request.others_username == connection_request[0]:
                # Eliminar la petició de la cua
                self.connection_requests[request.username].remove(connection_request)
                # Si es vol acceptar
                if request.bool: 
                    # Generar identificador i crear el chat privat
                    chat_id = str(uuid.uuid1())
                    self.private_chats[chat_id] = private_chat.PrivateChat()
                    # Tornar a afegir la petició a la cua, però amb l'identificador
                    self.connection_requests[request.username].append((request.others_username, chat_id))
                    self.logger.success(f"{colorama.Fore.YELLOW + request.username + colorama.Fore.RESET} ha acceptat la petició de chat de {colorama.Fore.YELLOW + request.others_username + colorama.Fore.RESET}")
                    return chat_id
                else:
                    self.logger.error(f"{colorama.Fore.YELLOW + request.username + colorama.Fore.RESET} ha denegat la petició de chat de {colorama.Fore.YELLOW + request.others_username + colorama.Fore.RESET}")
        return ""        
                
                
    # Funció per enviar un missatge a un chat privat
    def send_message_to(self, send):
        self.private_chats[send.chat_id].send_message(send)
        
        
    # Funció per rebre un missatge d'un chat privat
    def receive_message_from(self, receive):
        return self.private_chats[receive.chat_id].receive_message(receive)

    
message_broker = MessageBroker()