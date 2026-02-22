# 🤖 Chatbot WhatsApp -- Menu de Opções

Chatbot simples para WhatsApp com menu interativo, desenvolvido em
**Python + Flask**, utilizando **Twilio** como ponte para envio e
recebimento de mensagens.

Este projeto permite criar um menu com múltiplas opções e submenus,
ideal para:

-   Atendimento automatizado\
-   Informações institucionais\
-   Suporte básico\
-   Apresentação de serviços\
-   Encaminhamento para atendente

------------------------------------------------------------------------

## 🏗️ Tecnologias Utilizadas

-   Python 3\
-   Flask\
-   Twilio (WhatsApp Sandbox ou número oficial)\
-   ngrok (para testes locais)\
-   XML (TwiML)

------------------------------------------------------------------------

## 🚀 Como Executar o Projeto

### 1️⃣ Criar conta no Twilio

1.  Acesse: https://www.twilio.com\
2.  Crie uma conta (Trial é suficiente)\
3.  Vá em: Messaging → Try it out → Send a WhatsApp message\
4.  Ative o **WhatsApp Sandbox**\
5.  Conecte seu número enviando `join SEU-CODIGO` para o número do
    Sandbox

------------------------------------------------------------------------

### 2️⃣ Instalar dependências

``` bash
pip install -r requirements.txt
```

Se não tiver o arquivo `requirements.txt`:

``` bash
pip install flask python-dotenv
```

------------------------------------------------------------------------

### 3️⃣ Iniciar o servidor

``` bash
python main.py
```

O servidor ficará disponível em:

    http://localhost:5000

------------------------------------------------------------------------

### 4️⃣ Expor para internet (Webhook)

Instale o **ngrok**: https://ngrok.com

Execute:

``` bash
ngrok http 5000
```

Ele irá gerar uma URL HTTPS como:

    https://abc123.ngrok-free.dev

------------------------------------------------------------------------

### 5️⃣ Configurar Webhook no Twilio

No Console do Twilio → WhatsApp Sandbox:

Em **When a message comes in**, configure:

URL:

    https://SUA_URL_NGROK/webhook/whatsapp

Método: **POST**

Clique em **Save**.

------------------------------------------------------------------------

### 6️⃣ Testar o Bot

Envie uma mensagem para o número do Sandbox no WhatsApp.

Exemplo:

    oi

Você deverá receber o menu.

Digite:

    1
    2
    3
    4
    5

Para navegar nas opções.

------------------------------------------------------------------------

## 🧠 Estrutura do Projeto

    .
    ├── main.py
    ├── .env
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## 📌 Como Personalizar

### Alterar Menu Principal

Edite no `main.py`:

``` python
MENU = """
...
"""
```

### Alterar Respostas

Edite o dicionário:

``` python
OPCOES_MENU_PRINCIPAL
```

### Alterar Serviços

Edite:

``` python
SERVICOS_DETALHES
```

------------------------------------------------------------------------

## ⚠️ Importante

-   O estado do usuário atualmente é salvo **em memória**.\
-   Se o servidor reiniciar, o estado é perdido.\
-   Para produção, recomenda-se usar banco de dados (ex: Supabase,
    PostgreSQL).

------------------------------------------------------------------------

## 🔒 Ambiente de Produção

Para produção recomenda-se:

-   Rodar com `gunicorn`\
-   Usar servidor Linux (VPS)\
-   Configurar Nginx\
-   Utilizar HTTPS com domínio próprio\
-   Persistir estado no banco de dados

------------------------------------------------------------------------

## 📈 Próximas Evoluções

-   Integração com banco de dados\
-   Registro de histórico de mensagens\
-   Integração com IA\
-   Painel administrativo\
-   Atendimento humano (handoff)\
-   Deploy em VPS (Hostinger)

------------------------------------------------------------------------

## 👨‍💻 Autor

Projeto desenvolvido para estudo e implementação de automação de
atendimento via WhatsApp.
