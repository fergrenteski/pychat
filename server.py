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
    """Função para enviar mensagem para todos conectados

    Args:
        mensagem (String): Mensagem do remetente
        apelido_remetente (String, Optional): Apelido do Remente. Defaults to None.
    """
    # Percorre cada Apelido e Cliente
    for apelido, cliente in clientes.items():
        # Verifica se o apelido é igual do remetente
        if apelido != apelido_remetente:
            try:
                # Envia mensagem
                cliente.send(mensagem)
            except:
                # Caso erro Fecha conexão
                cliente.close()
                # Retira do dicionário
                del clientes[apelido]

# Loga Todas as mensagens
def log_message(origin, destination, mensagem):
    """Função para logar as ações no servidor

    Args:
        origin (String): Apelido da Origem
        destination (String): Apelido do Destino
        mensagem (String): Mensagem da Origem
    """
    time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"[{time}] {origin} -> {destination}: {mensagem}")

# Envia mensagem privada
def enviar_mensagem_privada(apelido_remetente, apelido_destino, mensagem):
    """Função para enviar mensagens privadas

    Args:
        apelido_remetente (String): Apelido do Remetente
        apelido_destino (String): Apelido do Destino
        mensagem (String): Mensagem do Remetente
    """
    # Busca o Cliente destino
    cliente_destino = clientes.get(apelido_destino)
    # Verifica se existe
    if cliente_destino:
        try:
            # Envia a mensagem para o cliente destino
            cliente_destino.send(f"(Privada) {apelido_remetente}: {mensagem}".encode())
            # Loga a mensagem privada
            log_message(apelido_remetente, apelido_destino, mensagem)
        except:
            # Fecha a conexão com o cliente
            cliente_destino.close()
            # Tira da Lista de clientes
            del clientes[apelido_destino]
    else:
        # Envia a mensagem para o cliente de origem que não foi encontrado usuário
        clientes[apelido_remetente].send(f"Usuário '{apelido_destino}' não encontrado.".encode())
        # Loga a mensagem
        log_message(apelido_remetente, f"Usuário '{apelido_destino}' não encontrado" , mensagem)


# Processo de Receber Mensagens
def receber_dados(cliente, apelido):
    """Função para receber os dados de cada cliente (Thread)

    Args:
        cliente (socket): Cliente a receber os dados
        apelido (String): Apelido do cliente
    """
    # Mensagem de boas vindas
    cliente.send("Bem-vindo ao chat!. Para sair, digite '/sair'. Para enviar uma mensagem privada: /privada <apelido> <mensagem>\n".encode())
    while True:
        try:
            # Recebe mensagens
            mensagem = cliente.recv(1024).decode()
            # Verifica se mensagem existe
            if mensagem:
                # Verifica de possui '/sair' na mensagem
                if '/sair' in mensagem.lower():
                    # Função de desconectar cliente
                    sair(cliente, apelido)
                    # Fecha tread do cliente
                    break
                elif mensagem.startswith('/privada '):
                    # Separa a mensagem em partes </privada> | <apelido> | <mensagem>
                    parts = mensagem.split(' ', 2)
                    # Verifica se a parte é maior que 3
                    if len(parts) >= 3:
                        # Define o apelido destino e a mensagem de acordo com as partes
                        apelido_destino, mensagem_privada = parts[1], parts[2]
                        # Envia a mensagem privada
                        enviar_mensagem_privada(apelido, apelido_destino, mensagem_privada)
                    else:
                        # Caso o formato fique incorreto ex: /privada exemplo
                        cliente.send("Formato incorreto. Use /privada <apelido> <mensagem>".encode())
                else:
                    # Envia mensagem para todos os clientes
                    broadcast(f'{apelido}: {mensagem}'.encode(), apelido_remetente=apelido)
                    # Loga mensagem para Todos
                    log_message(apelido, "Todos", mensagem)
        except:
            sair(cliente, apelido)
            break

# Função de desconectar cliente
def sair(cliente, apelido):
    """Função para desconectar cliente.

    Args:
        cliente (socket): Socket em que o cliente está conectado
        apelido (String): Apelido do cliente
    """
    # Fecha conexão com o cliente
    cliente.close()
    # Remove do dicionário
    del clientes[apelido]
    # Envia mensagem para todos em que o cliente desconectou
    broadcast(f'{apelido} desconectou do chat!'.encode(), apelido_remetente=apelido)
    # Loga mensagem
    log_message(apelido, 'Sistema', f'{apelido} desconectou do chat!')

# Processo de receber conexões
def receber_conexoes():
    while True:
        # Aceita as conexões
        cliente, endereco = servidor.accept()
        # Pega o Apelido do cliente
        apelido = cliente.recv(1024).decode()
        # Adiciona o cliente no dicionário key : value
        clientes[apelido] = cliente
        # Pega o ip e porta do endereço do cliente
        ip, porta = endereco
        # Loga a mensagem com IP e Porta
        log_message("Servidor", "Todos", f"{apelido} entrou no chat (IP: {ip}, Porta: {porta})")
        # Envia mensagem para todos indicando que o cliente entrou
        broadcast(f'{apelido} entrou no chat!'.encode())
        # Incializa a Thread do Cliente no servidor
        thread = threading.Thread(target=receber_dados, args=(cliente, apelido))
        thread.start()

# Início do sistema
print('Servidor está escutando...')
receber_conexoes()
