import redis
import colorama

# Importar altres classes
from server_log import ServerLog

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

class NameServer:
    
    def __init__(self):
        # Connexió a Redis
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)
        self.redis_client.delete('clients')
        # Inicialitzar logger
        self.logger = ServerLog(self)
        
    def exists_client(self, username):
        return self.redis_client.hexists('clients', username)
        
    # Funció per registrar l'adreça d'un client
    def register_client(self, client):
        # Comprovar que no estigui buit
        if client.username.replace(" ", "") == "":
            return (False, "El nom d'usuari no pot estar buit.")
        # Comprovar si ja hi ha un client connectat amb el mateix username
        if self.exists_client(client.username):
            return (False, "Aquest nom d'usuari ja està en ús actualment. Prova amb un altre.")
        self.redis_client.hset('clients', client.username, f"{client.ip}:{client.port}")
        # Imprimir log
        self.logger.log(f"Client registrat [username={client.username},ip={client.ip},port={client.port}]")
        return (True, "")
    
    
name_server = NameServer()