import grpc
import argparse
import uuid
from concurrent import futures
import time

# Importar classes generades
from proto import chat_pb2
from proto import chat_pb2_grpc
from server_log import ServerLog

# Importar altres classes
from name_server import name_server
from message_broker import message_broker
import private_chat

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
        response = name_server.register_client(client)
        return chat_pb2.Boolean(done=response[0], response=response[1])

    def ConnectChat(self, request, context):
        response = message_broker.connect_chat(request)
        if "id=" in response:
            return chat_pb2.Boolean(done=True, response=response.split("=")[1])
        return chat_pb2.Boolean(done=False, response=response)
    
    def ListenConnections(self, request, context):
        username = message_broker.listen_connections(request)
        return chat_pb2.Client(username=username)
    
    def AnswerConnection(self, request, context):
        response = message_broker.answer_connection(request)
        return chat_pb2.Boolean(response=response)

    def SendMessageTo(self, send, context):
        message_broker.send_message_to(send=send)
        return chat_pb2.Empty()
    
    def ReceiveMessageFrom(self, receive, context):
        message = message_broker.receive_message_from(receive)
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