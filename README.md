# Chat em Socket com Mensagens Privadas

Este projeto é um sistema de chat utilizando sockets em Python, onde é possível realizar comunicação em grupo e também enviar mensagens privadas para um usuário específico. O sistema conta com um servidor e clientes, que podem se conectar ao servidor e participar do chat.

## Pré-requisitos

### 1. Instalar Python

Se você ainda não possui o Python instalado, siga estas etapas para instalá-lo:

1. **Baixar Python**:
   - Acesse [python.org/downloads](https://www.python.org/downloads/) e baixe a versão mais recente do Python para o seu sistema operacional.
   
2. **Instalar Python**:
   - Durante a instalação, **certifique-se de marcar a opção** "Add Python to PATH" para poder usá-lo diretamente no terminal.

3. **Verificar a instalação**:
   - Após a instalação, abra o terminal (ou prompt de comando) e execute:
     ```bash
     python --version
     ```
   - Isso deve exibir a versão do Python instalada, confirmando que o Python está pronto para uso.

### 2. Instalar Dependências

Este projeto usa a biblioteca `python-dotenv` para carregar variáveis de ambiente. Para instalá-la, execute o seguinte comando no terminal:

```bash
pip install python-dotenv
```

## Configuração do Ambiente

1. **Crie o arquivo `.env`**: Na raiz do projeto, crie um arquivo chamado `.env` com as seguintes variáveis:

   ```env
   HOST=127.0.0.1  # Ou o IP do servidor, se estiver em outra máquina
   PORT=55555      # Porta para o servidor e o cliente se conectarem
   ```

   > **Nota**
   > Utilize o comando `ipconfig` no terminal para obtér o endereço de IP do seu computador
   > ```bash 
   > ipconfig


   - `HOST`: Especifique o endereço IP do servidor. Por exemplo, `127.0.0.1` para localhost ou o IP da máquina onde o servidor está rodando.
   - `PORT`: Defina a porta que o servidor usará para escutar conexões. O cliente também usará essa mesma porta para conectar-se.

## Como Iniciar o Servidor

1. **Configure o Servidor**:
   - Certifique-se de que o arquivo `.env` contém as configurações corretas para `HOST` e `PORT`.
   
2. **Execute o Servidor**:
   - Inicie o servidor executando o seguinte comando:
     ```bash
     python servidor.py
     ```

   - O servidor exibirá a mensagem `Servidor está escutando...`, indicando que está pronto para aceitar conexões de clientes.

## Como Iniciar o Cliente

1. **Configure o Cliente**:
   - Certifique-se de que o cliente também usa o mesmo arquivo `.env` configurado com o `HOST` e `PORT` corretos.

2. **Execute o Cliente**:
   - Inicie o cliente executando o seguinte comando:
     ```bash
     python cliente.py
     ```

3. **Escolha um Apelido**:
   - O cliente pedirá que você insira um apelido (nome de usuário) para usar no chat. Esse apelido será exibido aos outros usuários.

## Comandos no Chat

- Para enviar uma mensagem pública, digite a mensagem normalmente e pressione Enter.
- Para sair do chat, digite `/sair`.
- Para enviar uma mensagem privada, use o comando `/privada <apelido> <mensagem>`. Por exemplo:
  ```plaintext
  /privada João Olá, João! Esta é uma mensagem privada.
  ```
  - Se o usuário com o `apelido` especificado não estiver conectado, você receberá uma mensagem informando que o usuário não foi encontrado.

--- 