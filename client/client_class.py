import time
import colorama
import tkinter as tk
from tkinter import messagebox
import threading

from proto import chat_pb2

class Client:
    
    def __init__(self, username, ip, port, stub):
        # Inicialitzar biblioteca de colors per la terminal
        colorama.init()
        # Inicialitzar dades del client
        self.username = username
        self.ip = ip
        self.port = port
        self.stub = stub
        
    def open_chat(self, chat_id):
        
        def listen_messages(chat_list):
            while True:
                time.sleep(2)
                message = self.stub.ReceiveMessageFrom(chat_pb2.ReceiveMessage(chat_id=chat_id, username=self.username))
                if message.body != "":
                    chat_list.insert(tk.END, "[{}] {}\n".format(message.username, message.body))
        
        root = tk.Tk()  # I just used a very simple Tk window for the chat UI, this can be replaced by anything
        frame = tk.Frame(root, width=300, height=300)
        frame.pack()
        root.withdraw()
        root.deiconify() 
        
        def send_message(context):
            message = entry_message.get()  # retrieve message from the UI
            entry_message.delete(0, tk.END)
            if message != "":
                chat_list.insert(tk.END, "[{}] {}\n".format(self.username, message))
                self.stub.SendMessageTo(chat_pb2.SendMessage(chat_id=chat_id, username=self.username, body=message))  # send the Note to the server
                
        chat_list = tk.Text()
        chat_list.pack(side=tk.TOP)
        lbl_username = tk.Label(frame, text=self.username)
        lbl_username.pack(side=tk.LEFT)
        entry_message = tk.Entry(frame, bd=5)
        entry_message.bind('<Return>', send_message)
        entry_message.focus()
        entry_message.pack(side=tk.BOTTOM)
    
        threading.Thread(target=listen_messages, args=(chat_list,), daemon=True).start()

        frame.mainloop()
    
    def connect_chat(self):
        def connect():
            button["text"] = "Esperant resposta..."
            window.update()
            other = entry.get()
            response = self.stub.ConnectChat(chat_pb2.ConnectionRequest(username=self.username, others_username=other))
            if not response.done:
                messagebox.showerror("Error", response.response)
                button["text"] = "Connectar"
            else:
                window.destroy()
                threading.Thread(target=self.open_chat, args=(response.response,)).start()

        # Crear finestra tkinter
        window = tk.Tk()
        window.geometry("400x100")
        window.title("Connectant...")

        # Etiqueta i entrada per introduir el nom d'usuari de l'altre client
        tk.Label(window, text="Amb qui vols iniciar un chat?").pack()
        entry = tk.Entry(window)
        entry.pack()
        entry.focus_set()

        # Botó per connectar
        button = tk.Button(window, text="Connectar", command=connect)
        button.pack()

        # Bucle principal de la finestra de Tkinter
        window.mainloop()
       
    def accept_connection(self, root, username, bool):   
        root.destroy()
        response = self.stub.AnswerConnection(chat_pb2.AnswerRequest(username=self.username, others_username=username, bool=bool))
        threading.Thread(target=self.open_chat, args=(response.response,)).start()
     
    def listen_connections(self):
        def connection_request(username_wtc):
            root = tk.Tk()
            root.title(f"[{self.username}] Petició de chat")
            root.geometry("350x100")
            tk.Label(root, text=f"El client '{username_wtc.username}' vol iniciar un chat privat amb tu").pack()
            accept_btn = tk.Button(root, text="Accept", command=lambda: self.accept_connection(root, username_wtc.username, True), bg="#008000", bd=1, cursor="hand2")
            accept_btn.pack(side="left", padx=10)
            deny_btn = tk.Button(root, text="Deny", command=lambda: self.accept_connection(root, username_wtc.username, False), bg="#B22222", bd=1, cursor="hand2")
            deny_btn.pack(side="right", padx=10)
            root.mainloop()
            
        while True:
            username_wtc = self.stub.ListenConnections(chat_pb2.Client(username=self.username))
            connection_request(username_wtc=username_wtc)
    
    def send_message(self):
        while True:
            text = input()
            message = chat_pb2.Message()
            message.username = self.username
            message.body = text
            self.stub.SendMessage(message)
        
    def receive_message(self):
        user = chat_pb2.Client()
        user.username = self.username
        while True:
            time.sleep(2)
            message = self.stub.ReceiveMessage(user)
            if message.body != "":
                print(f"[{message.username}] {message.body}")