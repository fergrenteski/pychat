import threading
import socket
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do Cliente
host = os.getenv('HOST', '127.0.0.1')  # localhost como padrão
port = int(os.getenv('PORT', 55555))  # 55555 como padrão

# Input de apelido
apelido = input("Escolha um apelido: ")

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

# Envia o apelido ao servidor imediatamente após a conexão
cliente.send(apelido.encode())

# Função de Receber mensagens
def receber_mensagens():
    while True:
        try:
            # Pega mensagens
            mensagem = cliente.recv(1024).decode()
            # Verifica se a mensagem existe
            if mensagem:
                # Exibe a mensagem
                print(mensagem)
        except:
            # Caso de erro exibe mensagem de configuração
            print("Conexão encerrada pelo servidor.")
            # Fecha conexão
            cliente.close()
            # Encerra a Thread
            break

# Função de Enviar mensagens
def enviar_mensagens():
    while True:
        # Input de mensagem
        mensagem = input("Digite: ").strip()
        # Verifica se existe mensagem
        if mensagem:
            # Verifica se contém '/sair'
            if mensagem.lower() == '/sair':
                # Envia mensagem pro servidor
                cliente.send(mensagem.encode())
                # Exibe que você saiu
                print("Você saiu do chat.")
                # Fecha conexão com o servidor
                cliente.close()
                # Encerra a Thread de enviar mensagens
                break
            else:
                # Envia mensagem
                cliente.send(mensagem.encode())

# Inicia as threads para receber e enviar mensagens
receber_thread = threading.Thread(target=receber_mensagens)
receber_thread.start()

enviar_thread = threading.Thread(target=enviar_mensagens)
enviar_thread.start()
