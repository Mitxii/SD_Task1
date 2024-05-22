import threading

# Importar altres classes
from server_log import ServerLog

class PrivateChat: 
    
    def __init__(self):
        # Inicialitzar llista de missatges i locker per bloquejar la lectura i escriptura simultània
        self.queue = list()
        self.lock = threading.Lock()
        # Inicialitzar logger
        self.logger = ServerLog(self)
        
    def send_message(self, message):
        with self.lock:
            self.queue.append(message)
        
    def receive_message(self, username):
        with self.lock:
            if self.queue and self.queue[0].username != username.username:
                return self.queue.pop(0)
            else:
                return ""