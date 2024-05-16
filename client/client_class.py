import time

from proto import chat_pb2

class Client:
    
    def __init__(self, username, ip, port, stub):
        self.username = username
        self.ip = ip
        self.port = port
        self.stub = stub
    
    def send_message(self):
        while True:
            text = input()
            message = chat_pb2.Message()
            message.username = self.username
            message.body = text
            self.stub.SendMessage(message)
        
    def receive_message(self):
        user = chat_pb2.Client()
        user.username = self.username
        while True:
            time.sleep(2)
            message = self.stub.ReceiveMessage(user)
            if message.body != "":
                print(f"[{message.username}] {message.body}")