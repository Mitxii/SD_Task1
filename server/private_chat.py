import threading

# Importar altres classes
from server_log import ServerLog

# Classe pels chats privats entre dos clients
class PrivateChat: 
    
    # Constructor
    def __init__(self):
        # Inicialitzar logger
        self.logger = ServerLog(self)
        # Inicialitzar llista de missatges i locker per bloquejar la lectura i escriptura simultània
        self.queue = list()
        self.lock = threading.Lock()
        
    
    # Funció per enviar un missatge
    def send_message(self, message):
        with self.lock:
            self.queue.append(message)
        
        
    # Funció per rebre un missatge
    def receive_message(self, username):
        with self.lock:
            # Comprovar que només es pugui llegir i eliminar el missatge de la cua si l'ha enviat l'altre client
            if self.queue and self.queue[0].username != username.username:
                return self.queue.pop(0)
            else:
                return ""