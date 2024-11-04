import threading
import socket
from datetime import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do Servidor
host = os.getenv('HOST', '127.0.0.1')  # localhost como padrão
port = int(os.getenv('PORT', 55555))  # 55555 como padrão

# Coloca o Servidor para escutar conexões
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen()

# Dicionário para armazenar apelidos e clientes
clientes = {}

# Envia mensagens para todos os clientes
def broadcast(mensagem, apelido_remetente=None):
    # percorre todos os clientes
    for apelido, cliente in clientes.items():
        # Envia a mensagem apenas para outros clientes, não para o remetente
        if apelido != apelido_remetente:
            try:
                cliente.send(mensagem)
            except:
                # Se houver um erro ao enviar, remove o cliente
                cliente.close()
                del clientes[apelido]

# Loga Todas as mensagens
def log_message(origin, destination, mensagem):
    # Obtém a data atual para logar no sistema
    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"[{time}] {origin} -> {destination}: {mensagem}")

# Processo de Receber Mensagens
def receber_dados(cliente, apelido):
    cliente.send(
        "Bem-vindo ao chat!.\n".encode())
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem:
                    # Envia para todos
                    broadcast(f'{apelido}: {mensagem}'.encode(), apelido_remetente=apelido)

                    # Loga no Sistema
                    log_message(apelido, "Todos", mensagem)
        except:
            break

# Processo de receber conexões
def receber_conexoes():
    while True:
        # Aceita conexões
        cliente, endereco = servidor.accept()

        # Pega o apelido do cliente
        apelido = cliente.recv(1024).decode()

        # Adiciona na lista
        clientes[apelido] = cliente

        # Obtém o IP e a porta do cliente
        ip, porta = endereco

        # Loga a entrada do cliente no servidor com IP e porta
        log_message("Servidor", "Todos", f"{apelido} entrou no chat (IP: {ip}, Porta: {porta})")

        # Loga a entrada do cliente no servidor
        log_message("Servidor", "Todos", f"{apelido} entrou no chat")

        # Envia uma mensagem de entrada para todos os clientes
        broadcast(f'{apelido} entrou no chat!'.encode())

        # Cria e inicia uma nova thread para o cliente
        thread = threading.Thread(target=receber_dados, args=(cliente, apelido))
        thread.start()



# Início do sistema
print('Servidor está escutando...')
receber_conexoes()
