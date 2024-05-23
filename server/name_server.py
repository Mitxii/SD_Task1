import redis
import colorama

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
    
    
name_server = NameServer()