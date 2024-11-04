import threading
import socket
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do Cliente
host = os.getenv('HOST', '127.0.0.1')  # localhost como padrão
port = int(os.getenv('PORT', 55555))  # 55555 como padrão

apelido = input("Escolha um apelido: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

# Envia o apelido ao servidor imediatamente após a conexão
cliente.send(apelido.encode())

def receber_mensagens():
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem:  # Adicionado para evitar mensagens vazias
                print(mensagem)
        except:
            print(f"Saindo...")
            cliente.close()
            break

def enviar_mensagens():
    while True:
        # Input de mensagem
        mensagem = input("Digite: ").strip()
        if mensagem:
            cliente.send(f'{apelido}: {mensagem}'.encode())

# Inicia as threads para receber e enviar mensagens
receber_thread = threading.Thread(target=receber_mensagens)
receber_thread.start()

enviar_thread = threading.Thread(target=enviar_mensagens)
enviar_thread.start()
