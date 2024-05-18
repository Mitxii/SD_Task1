import grpc
import argparse
from concurrent import futures
import time

# Importar classes generades
from proto import chat_pb2
from proto import chat_pb2_grpc
from server_log import ServerLog

# Importar altres classes
from name_server import name_server
from private_chat import private_chat

# Crear l'analitzador d'arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)

# Obtenir el port
port = parser.parse_args().port

class ServerServicer(chat_pb2_grpc.ChatServerServicer):
    
    def __init__(self):
        # Inicialitzar logger
        self.logger = ServerLog(self)
        
    def RegisterClient(self, client, context):
        boolean = name_server.register_client(client)
        return chat_pb2.Boolean(bool=boolean)

    def SendMessage(self, message, context):
        private_chat.send_message(message)
        return chat_pb2.Empty()
    
    def ReceiveMessage(self, client, context):
        message = private_chat.receive_message(client)
        response = chat_pb2.Message(username="")
        if message != "":
            response.username = message.username
            response.body = message.body
        return response

# Crear servidor gRPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
servicer = ServerServicer()
chat_pb2_grpc.add_ChatServerServicer_to_server(servicer, server)
servicer.logger.log(f'Starting server. Listening on port {port}...')
server.add_insecure_port(f'0.0.0.0:{port}')
server.start()

# Bucle infinit
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)