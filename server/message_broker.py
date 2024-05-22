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

class MessageBroker:
    
    def __init__(self):
        # Inicialitzar logger
        self.logger = ServerLog(self)
        # Inicialitzar cues de peticions de connexió
        self.connection_requests = {}
        # Inicialitzar chats privats oberts
        self.private_chats = {}
        
    def connect_chat(self, request):
        self.logger.log(f"{colorama.Fore.YELLOW}{request.username}{colorama.Fore.RESET} vol començar un chat privat amb {colorama.Fore.YELLOW}{request.others_username}{colorama.Fore.RESET}")
        if request.username == request.others_username:
            return "No pots obrir un chat amb tu mateix"
        elif not name_server.exists_client(request.others_username):
            self.logger.error(f"No s'ha trobat el client {request.others_username}")
            return f"No s'ha trobat el client {request.others_username}."
        else:
            self.connection_requests[request.others_username] = []
            self.connection_requests[request.others_username].append((request.username, "id"))
            self.logger.log(f"{request.username} afegit a la cua de {request.others_username} -> {self.connection_requests[request.others_username]}")

            while True:
                time.sleep(1)
                for connection_request in self.connection_requests[request.others_username]:
                    if request.username == connection_request[0] and connection_request[1] == "":
                        self.connection_requests[request.others_username].remove(connection_request)
                        return f"El client {request.others_username} no ha acceptat la petició."
                    elif request.username == connection_request[0] and "id" not in connection_request[1] and "waiting" not in connection_request[1]:
                        chat_id = connection_request[1]
                        self.connection_requests[request.others_username].remove(connection_request)
                        return f"id={chat_id}"
    
    def listen_connections(self, request):
        while True:
            time.sleep(2)
            if request.username in self.connection_requests and self.connection_requests[request.username] and self.connection_requests[request.username][0][1] == "id":
                self.connection_requests[request.username][0][1] == "waiting"
                return self.connection_requests[request.username][0][0]
            
    def answer_connection(self, request):
        input = ""
        if request.bool:
            chat_id = str(uuid.uuid1())
            self.private_chats[chat_id] = private_chat.PrivateChat()
            input = chat_id   
        for connection_request in self.connection_requests[request.username]:
            if request.others_username == connection_request[0]:
                self.connection_requests[request.username].remove(connection_request)
                self.connection_requests[request.username].append((request.others_username, input))
        return input        
                
    def send_message_to(self, send):
        self.private_chats[send.chat_id].send_message(send)
        
    def receive_message_from(self, receive):
        return self.private_chats[receive.chat_id].receive_message(receive)
    
message_broker = MessageBroker()