import colorama
from datetime import datetime

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

# Classe per imprimir logs al servidor d'una forma més visual
class ServerLog:
    
    # Constructor
    def __init__(self, source):
        self.source = source.__class__.__name__
        match self.source:
            case "MessageBroker":
                self.back_color = colorama.Back.MAGENTA
            case "NameServer":
                self.back_color = colorama.Back.YELLOW
            case default:
                self.back_color = colorama.Back.WHITE
        
        
    def get_timestamp(ctx=False):
        return datetime.now().strftime("%H:%M")
    
        
    # Funció per imprimir un missatge de log
    def log(self, log):
        timestamp = self.get_timestamp()
        if self.source != "ServerServicer":
            print(f"{self.back_color + timestamp}[{self.source}]{colorama.Back.RESET} {log}")
        else:
            print(f"{colorama.Back.CYAN + timestamp}[Server]{colorama.Back.RESET} {log}")
          
          
    # Funció per imprimir un missatge d'error  
    def error(self, error):
        timestamp = self.get_timestamp()
        if self.source != "ServerServicer":
            print(f"{self.back_color + timestamp}[{self.source}]{colorama.Back.RESET}{colorama.Back.RED} ✖ {colorama.Back.RESET} {error}")
        else:
            print(f"{colorama.Back.CYAN + timestamp}[Server]{colorama.Back.RESET}{colorama.Back.RED} ✖ {colorama.Back.RESET} {error}")
            
    
    # Funció per imprimir un missatge d'èxit  
    def success(self, succ):
        timestamp = self.get_timestamp()
        if self.source != "ServerServicer":
            print(f"{self.back_color + timestamp}[{self.source}]{colorama.Back.RESET}{colorama.Back.GREEN} ✔ {colorama.Back.RESET} {succ}")
        else:
            print(f"{colorama.Back.CYAN + timestamp}[Server]{colorama.Back.RESET}{colorama.Back.GREEN} ✔ {colorama.Back.RESET} {succ}")