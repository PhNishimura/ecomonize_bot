-----

# Bot de Controle de Gastos para Telegram

Este é um bot simples para Telegram, desenvolvido em Python, que ajuda você a registrar e controlar seus gastos mensais de forma rápida e prática.

## ✨ Funcionalidades

  - **Adicionar Gastos:** Registre um novo gasto enviando uma mensagem simples com o local e o valor.
  - **Data Automática e Manual:** O bot utiliza a data atual por padrão, mas permite que você especifique uma data diferente.
  - **Cálculo Mensal:** Após cada registro, o bot informa o valor total gasto no mês corrente.
  - **Armazenamento Local:** Todos os gastos são salvos em um arquivo local chamado `gastos.json`, facilitando o backup e a visualização dos dados.

## 🔧 Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

  - [Python 3.8+](https://www.python.org/downloads/)
  - A biblioteca `python-telegram-bot`

## ⚙️ Instalação, Configuração e Funcionamento

Siga os passos abaixo para colocar seu bot em funcionamento.

1.  **Clone o Repositório**

    ```bash
    # Se estiver usando Git
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DA_PASTA>
    ```

    Ou simplesmente baixe o arquivo `botEconomia_noTelegram.py` para um diretório em seu computador.

2.  **Instale as Dependências**
    Abra seu terminal ou prompt de comando e instale a biblioteca necessária:

    ```bash
    pip install python-telegram-bot
    ```

3.  **Obtenha seu Token do Telegram**

      - Abra o Telegram e procure pelo bot `@BotFather`.
      - Inicie uma conversa com ele e digite o comando `/newbot`.
      - Siga as instruções para dar um nome e um nome de usuário para o seu bot.
      - Ao final, o BotFather fornecerá um **token de acesso**. Copie este token.

4.  **Configure o Token no Código**

      - Abra o arquivo de código (`botEconomia_noTelegram.py`).
      - Encontre a linha:
        ```python
        TOKEN = "SEU_TOKEN_AQUI"
        ```
      - Substitua `"SEU_TOKEN_AQUI"` pelo token que você copiou do BotFather.

5. **Como Manter o Bot Funcionando**


      - Para que seu bot responda no Telegram, o arquivo Python (`botEconomia_noTelegram.py`) precisa estar em execução constante. Se o script parar, o bot ficará offline.


Existem duas formas principais de executá-lo:

* **Na sua máquina local:** Execute `python botEconomia_noTelegram.py` no seu computador. Esta opção é ideal para testes, mas lembre-se: o bot só funcionará enquanto seu PC estiver ligado e o programa rodando.

* **Em um servidor ou plataforma de hospedagem:** Para que o bot fique online 24/7, o script precisa ser executado em um ambiente que nunca desliga, como um servidor na nuvem (VPS) ou uma plataforma de hospedagem de aplicações.


  

## ▶️ Como Executar

Com tudo configurado, execute o bot usando o seguinte comando no seu terminal, na pasta onde o arquivo está salvo:

```bash
python botEconomia_noTelegram.py
```

Se tudo estiver correto, você verá a mensagem "Bot iniciado...." no terminal.

## 💬 Como Usar o Bot

1.  **Inicie a Conversa**
    Abra o Telegram, encontre o seu bot e envie o comando:

    ```
    /start
    ```

2.  **Adicione um Gasto (Data Atual)**
    Envie uma mensagem no formato `Lugar, Valor`:

    ```
    Padaria, 25.50
    ```

3.  **Adicione um Gasto (Data Específica)**
    Envie uma mensagem no formato `Lugar, Valor, DD/MM/AAAA`:

    ```
    Cinema, 45.00, 01/08/2025
    ```

O bot responderá confirmando que o gasto foi salvo e mostrando o total gasto no mês.
