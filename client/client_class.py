import time
import colorama
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

# Importar classes gRPC
from proto import chat_pb2

# Inicialitzar biblioteca de colors per la terminal
colorama.init()

# Classe per guardar les dades dels clients i accedir a les funcions
class Client:
    
    # Constructor
    def __init__(self, username, ip, port, stub):
        self.username = username
        self.ip = ip
        self.port = port
        self.stub = stub
        # Inicialitzar llista de chats privats oberts
        self.private_chats = set()
        
        
    # Funció per obrir un chat privat (finestra, lectura i escriptura de missatges)
    def open_chat(self, chat_id, other):
        
        # Funció per imprimir un missatge al chat
        def display_message(message, alignment):
            chat_display.config(state="normal")
            chat_display.insert(END, f"{message}\n", alignment)
            chat_display.tag_configure(alignment, justify=alignment)
            chat_display.config(state="disabled")
            chat_display.yview(END)
        
        # Funció per enviar un missatge
        def send_message(ctx=None):
            message = entry_msg.get()
            if message != "":
                display_message(message, "right")
                entry_msg.delete(0, END)
                self.stub.SendMessageTo(chat_pb2.SendMessage(chat_id=chat_id, username=self.username, body=message))
               
        # Configurar finestra de chat privat amb tkinter
        root = Tk()
        root.title(f"[{self.username}] {other}")
        root.geometry("400x500")
        # Frame per als inputs (missatges a enviar)
        input_frame = Frame(root)
        input_frame.pack(pady=5, padx=10, fill=X, side=BOTTOM)
        send_btn = Button(input_frame, text="Enviar", command=send_message, cursor="hand2")
        send_btn.pack(side=RIGHT)
        entry_label = Label(input_frame, text="Tu:")
        entry_label.pack(side=LEFT)
        entry_msg = Entry(input_frame)
        entry_msg.pack(fill=X, padx=(0, 10))
        entry_msg.bind("<Return>", send_message)
        entry_msg.focus_set()
        # ScrolledText per mostrar els missatges
        chat_display = scrolledtext.ScrolledText(root, wrap=WORD, state="disabled")
        chat_display.pack(pady=10, padx=10, fill=BOTH, expand=True)
        chat_display.configure(padx=10, pady=10)
    
        # Funció per anar escoltant missatges
        def listen_messages():
            while True:
                time.sleep(.5)
                message = self.stub.ReceiveMessageFrom(chat_pb2.ReceiveMessage(chat_id=chat_id, username=self.username))
                if message.username == "disconnect":
                    entry_msg.destroy()
                    send_btn.destroy()
                    entry_label.destroy()
                    Label(input_frame, text=f"{other} s'ha desconnectat del chat").pack()
                    self.private_chats.remove(other)
                elif message.body != "":
                    display_message(message.body, "left")
                    
        # Llançar thread per escoltar missatges
        threading.Thread(target=listen_messages).start()
        
        # Funció per alliberar el chat al tancar la finestra
        def close_chat():
            if other in self.private_chats:
                self.private_chats.remove(other)
                self.stub.SendMessageTo(chat_pb2.SendMessage(chat_id=chat_id, username="disconnect"))
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", close_chat)

        # Llançar finestra
        root.mainloop()
    
    
    # Funció per sol·licitar un chat privat
    def connect_chat(self):
        
        # Funció per sol·licitar el chat
        def connect(ctx=False):
            button["text"] = "Connectant..."
            root.update()
            other = entry.get()
            if other in self.private_chats:
                messagebox.showerror("Error", "Ja tens un chat obert amb aquest client.")
                entry.delete(0, END)
                button["text"] = "Connectar"
                return
            response = self.stub.ConnectChat(chat_pb2.ConnectionRequest(username=self.username, others_username=other))
            if not response.done:
                messagebox.showerror("Error", response.response)
                entry.delete(0, END)
                button["text"] = "Connectar"
            else:
                root.destroy()
                self.private_chats.add(other)
                threading.Thread(target=self.open_chat, args=(response.response, other,)).start()

        # Configurar finestra per sol·licitar chat privat
        root = Tk()
        root.title(f"[{self.username}] Connectar chat")
        root.geometry("400x105")
        # Etiqueta i entrada per introduir el nom d'usuari de l'altre client
        Label(root, text="Amb qui vols iniciar un chat?").pack(pady=(5, 0))
        entry = Entry(root)
        entry.pack()
        entry.bind("<Return>", connect)
        entry.focus_set()
        # Botó per connectar
        button = Button(root, text="Connectar", command=connect, cursor="hand2")
        button.pack(pady=5)

        # Llançar finestra
        root.mainloop()
       
     
    # Funció per escoltar peticions de chat
    def listen_connections(self):
        
        # Funció per respondre una sol·licitud de chat (acceptar o denegar)
        def answer_connection(username, bool):
            root.destroy()
            response = self.stub.AnswerConnection(chat_pb2.AnswerRequest(username=self.username, others_username=username, bool=bool))
            if bool: 
                self.private_chats.add(username)
                threading.Thread(target=self.open_chat, args=(response.response, username,)).start()

        while True:
            # Obtenir el primer client de la llista de peticions
            username_wtc = self.stub.ListenConnections(chat_pb2.Client(username=self.username))
            
            # Configurar finestra per respondre la sol·licitud
            root = Tk()
            root.title(f"[{self.username}] Petició de chat")
            root.geometry("350x90")
            Label(root, text=f"'{username_wtc.username}' vol iniciar un chat privat.").pack(pady=(5, 0))
            # Frame pels botons d'acceptar i denegar
            btn_frame = Frame(root)
            btn_frame.pack(pady=5)
            deny_btn = Button(btn_frame, text="Denegar", command=lambda: answer_connection(username_wtc.username, False), bg="#B22222", cursor="hand2")
            deny_btn.pack(side=LEFT, fill=Y, padx=10, pady=5)
            Label(btn_frame, width=10).pack(side=LEFT)
            accept_btn = Button(btn_frame, text="Acceptar", command=lambda: answer_connection(username_wtc.username, True), bg="#008000", cursor="hand2")
            accept_btn.pack(side=LEFT, fill=Y, padx=10, pady=5)

            # Llançar finestra
            root.mainloop()