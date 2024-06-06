import grpc
import pika
import colorama
import yaml
import argparse
import os
import threading
import time
import re

# Importar classes gRPC
from proto import chat_pb2
from proto import chat_pb2_grpc

# Importar altres classes
from client_class import Client

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

# Obtenir dades del fitxer config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
server_ip = config["server_ip"]
grpc_port = config["server_grpc_port"]
rabbit_port = config["server_rabbit_port"]

# Crear l'analitzador d'arguments per obtenir l'adreça del client (ip:port)
parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str)
parser.add_argument("--port", type=int)
ip = parser.parse_args().ip
port = parser.parse_args().port

# Obrir canal gRPC i crear un stub
channel = grpc.insecure_channel(f"{server_ip}:{grpc_port}")
stub = chat_pb2_grpc.ChatServerStub(channel)

# Bucle per obtenir un nom d'usuari disponible
while True:
    # Demanar nom d'usuari
    username = input("Introdueix usuari: ")
    # Eliminar caràcters especials
    username = re.sub(r"[^A-Za-z0-9\s]", "", username)
    # Registrar client
    response = stub.RegisterClient(chat_pb2.Client(username=username, ip=ip, port=port))
    if response.done:
        # Crear instància del client
        client = Client(username, ip, port, stub)
        print(f"{colorama.Back.GREEN} ✔ {colorama.Back.RESET} T'has registrat correctament.")
        break
    else:
        print(f"{colorama.Back.RED} ✖ {colorama.Back.RESET} {response.response}")

# Esperar mig segon i netejar terminal
time.sleep(0.5)
os.system("cls" if os.name == "nt" else "clear")

# Obrir connexió amb el servidor RabbitMQ
parameters = pika.ConnectionParameters(host=server_ip, port=rabbit_port)
connection = pika.BlockingConnection(parameters)
rabbit = connection.channel()

# Escoltar peticions de chats privats
threading.Thread(target=client.listen_connections).start()
# Enviar senyals mentre segueixi actiu
threading.Thread(target=client.heartbeat).start()

os.system(f"echo 'Bones, \033[33m{username}\\033]0;{username}\\007\033[0m!'")
print(f"\n\t{colorama.Back.YELLOW + colorama.Fore.BLACK} [P]rivat | [G]rupal | [D]escobrir | [I]nsults | [S]ortir {colorama.Back.RESET + colorama.Fore.RESET}\n")

# Bucle principal del client
while True:
    option = input("Opció: ").upper()
    match option:
        case "P":
            threading.Thread(target=client.connect_chat).start()
            
        case "G":
            break
        
        case "D":
            client.discover_chats()
            break
        
        case "I":
            break
        
        case "S":
            print(f"Fins aviat {colorama.Fore.YELLOW + username + colorama.Fore.RESET}!")
            break
        
        case default:
            print(f"{colorama.Back.RED} ✖ {colorama.Back.RESET} Opció invàlida. Tria'n una de vàlida.{colorama.Fore.RESET}")
        
