import redis
import colorama
import threading

# Importar altres classes
from server_log import ServerLog

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

# Classe per registrar tots els clients utilitzant REDIS
class NameServer:
    
    # Constructor
    def __init__(self):
        # Inicialitzar logger
        self.logger = ServerLog(self)
        # Connectar a Redis
        self.redis_client = redis.StrictRedis(host="localhost", port=6379)
        self.redis_client.delete("clients")
        # Inicialitzar timers per gestionar desconnexions
        self.timers = {}
        
    
    # Funció per comprovar si un client existeix (està connectat)
    def exists_client(self, username):
        return self.redis_client.hexists("clients", username)
        
        
    # Funció per registrar un client
    def register_client(self, client):
        # Comprovar que el nom d'usuari no estigui buit
        if client.username.replace(" ", "") == "":
            self.logger.error("No s'ha pogut registrar el client (nom d'usuari buit)")
            return (False, "El nom d'usuari no pot estar buit.")
        # Comprovar si ja hi ha un client connectat amb el mateix nom d'usuari
        if self.exists_client(client.username):
            self.logger.error("No s'ha pogut registrar el client (nom d'usuari en ús)")
            return (False, "Aquest nom d'usuari està actualment en ús.")
        
        # Registrar client
        self.redis_client.hset("clients", client.username, f"{client.ip}:{client.port}")
        self.logger.success(f"Client registrat {colorama.Fore.YELLOW}[username={client.username},ip={client.ip},port={client.port}]{colorama.Fore.RESET}")
        return (True, "")
    
    
    # Funció per desconnectar un client
    def disconnect_client(self, client):
        # Eliminar client de redis
        self.redis_client.hdel("clients", client.username)
        self.logger.success(f"El client {colorama.Fore.YELLOW + client.username + colorama.Fore.RESET} s'ha desconnectat")
        # Eliminar timer
        if client.username in self.timers:
            self.timers.pop(client.username)
    
    
    # Funció per enviar una senyal indicant que un client segueix actiu
    def heartbeat(self, client):
        # Si el client ja té un timer assigant, cancelar-lo
        if client.username in self.timers:
            self.timers[client.username].cancel()
        # Crear timer nou i assignar-lo al client
        timer = threading.Timer(5, self.disconnect_client, args=(client,))
        self.timers[client.username] = timer
        # Iniciar timer
        timer.start()
    
    
name_server = NameServer()