import threading

class PrivateChat: 
    
    def __init__(self):
        self.queue = list()
        self.lock = threading.Lock()
        
    def send_message(self, message):
        with self.lock:
            self.queue.append(message)
        
    def receive_message(self, username):
            with self.lock:
                if self.queue and self.queue[0].username != username.username:
                    return self.queue.pop(0)
                else:
                    return ""
        
    
private_chat = PrivateChat()