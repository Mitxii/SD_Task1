import grpc
import argparse
from concurrent import futures
import time

from proto import chat_pb2
from proto import chat_pb2_grpc
from private_chat import private_chat

# Crear l'analitzador d'arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)

# Obtenir el port
port = parser.parse_args().port

class ServerServicer(chat_pb2_grpc.ChatServerServicer):

    def SendMessage(self, message, context):
        private_chat.send_message(message)
        return chat_pb2.Empty()
    
    def ReceiveMessage(self, client, context):
        message = private_chat.receive_message(client)
        response = chat_pb2.Message()
        if message == "":
            response.username = ""
        else:
            response.username = message.username
            response.body = message.body
        return response

# Crear servidor gRPC
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
chat_pb2_grpc.add_ChatServerServicer_to_server(ServerServicer(), server)
print(f'Starting server. Listening on port {port}.')
server.add_insecure_port(f'0.0.0.0:{port}')
server.start()

# Bucle infinit
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)