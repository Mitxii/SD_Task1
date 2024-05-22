import grpc
import colorama
import yaml
import argparse
import os
import threading
import time
import subprocess

# Importar classes generades
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

while True:
    # Demanar nom d'usuari
    username = input("Introdueix usuari: ")

    # Registrar client
    response = stub.RegisterClient(chat_pb2.Client(username=username, ip=ip, port=port))
    if response.done:
        print(colorama.Fore.GREEN + "T'has registrat correctament." + colorama.Fore.RESET)
        break
    else:
        print(colorama.Fore.RED + response.response + colorama.Fore.RESET)

# Crear client
client = Client(username, ip, port, stub)

# Esperar un segon i netejar terminal
time.sleep(0.5)
os.system('cls' if os.name == 'nt' else 'clear')
os.system(f"echo 'Bones, \033[33m{username}\\033]0;{username}\\007\033[0m!'")

# Escoltar peticions de chats privats
threading.Thread(target=client.listen_connections).start()

# Bucle principal del client
print(f"\n\t{colorama.Back.YELLOW}{colorama.Fore.BLACK} [P]rivat | [G]rupal | [D]escobrir | [I]nsults | [S]ortir {colorama.Back.RESET}{colorama.Fore.RESET}\n")
while True:
    option = input("Opció: ").upper()

    if option == "P":
        threading.Thread(target=client.connect_chat).start()
        pass
    elif option == "G":
        pass
    elif option == "D":
        pass
    elif option == "I":
        pass
    elif option == "S":
        print("Fins aviat " + colorama.Fore.YELLOW + f"{username}" + colorama.Fore.RESET + "!")
        break
    else:
        print(colorama.Fore.RED + "Opció invàlida. Tria'n una de vàlida." + colorama.Fore.RESET)
        
# Iniciar chat (enviar i llegir missatges)
threading.Thread(target=client.send_message).start()
threading.Thread(target=client.receive_message).start()
