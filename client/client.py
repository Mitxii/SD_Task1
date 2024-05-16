import grpc
import yaml
import argparse
import os
import threading
import time

from proto import chat_pb2
from proto import chat_pb2_grpc
import client_class

# Obtenir dades del fitxer config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
server_ip = config["server_ip"]
server_port = config["server_port"]

# Crear l'analitzador d'arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str)
parser.add_argument('--port', type=int)

# Obtenir adreça del client (ip:port)
ip = parser.parse_args().ip
port = parser.parse_args().port

# Obrir canal gRPC i crear un stub
channel = grpc.insecure_channel(f"{server_ip}:{server_port}")
stub = chat_pb2_grpc.ChatServerStub(channel)

# Demanar nom d'usuari
username = input("Enter username: ")

# Crear client
client = client_class.Client(username, ip, port, stub)

# Netejar terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Iniciar chat (enviar i llegir missatges)
threading.Thread(target=client.send_message).start()
threading.Thread(target=client.receive_message).start()
