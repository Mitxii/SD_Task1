import colorama

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

class ServerLog:
    
    def __init__(self, source):
        self.source = source.__class__.__name__
        
    def log(self, log):
        if self.source != "ServerServicer":
            print(f"{colorama.Back.YELLOW}[{self.source}]{colorama.Back.RESET} {log}")
        else:
            print(f"{colorama.Back.CYAN}[Server]{colorama.Back.RESET} {log}")
            
    def error(self, error):
        if self.source != "ServerServicer":
            print(f"{colorama.Back.YELLOW}[{self.source}]{colorama.Back.RESET} {colorama.Fore.RED}{error}{colorama.Fore.RESET}")
        else:
            print(f"{colorama.Back.CYAN}[Server]{colorama.Back.RESET} {colorama.Fore.RED}{error}{colorama.Fore.RESET}")