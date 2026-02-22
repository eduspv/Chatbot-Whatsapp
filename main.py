"""
Chatbot WhatsApp simples com menu de opções.
Usa Twilio como ponte para o WhatsApp (Sandbox ou número oficial Twilio).
"""

import os
import logging
import xml.etree.ElementTree as ET
from flask import Flask, request, Response
from dotenv import load_dotenv

load_dotenv()

# Log no terminal para ver quando o Twilio chama o webhook
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ----------------------------
# 1) Mensagens (menu e textos)
# ----------------------------

MENU = """
*Menu – Escolha uma opção:*

1️⃣ Informações gerais
2️⃣ Horário de funcionamento
3️⃣ Contato / Suporte
4️⃣ Serviços oferecidos
5️⃣ Falar com atendente

Digite o *número* da opção desejada (ex: 1)
""".strip()

OPCOES_MENU_PRINCIPAL = {
    "1": "📋 *Informações gerais*\n\nAqui você encontra as informações principais. Para dúvidas específicas, use o menu ou opção 5.",
    "2": "🕐 *Horário de funcionamento*\n\nSegunda a Sexta: 8h às 18h\nSábado: 8h às 12h\nDomingo e feriados: fechado",
    "3": "📞 *Contato / Suporte*\n\nE-mail: contato@exemplo.com\nTelefone: (00) 0000-0000\nWhatsApp: este número",
    "5": "👤 *Atendente*\n\nEm breve um atendente responderá. Aguarde alguns instantes. Se for urgente, ligue para (00) 0000-0000.",
}

SERVICOS_MENU = """
🛠 *Serviços oferecidos* — escolha um:

1️⃣ Biodescontaminação assistida e certificada
2️⃣ SASMUV (controle de vetores)
3️⃣ Banho no leito
4️⃣ Saúde Mental

Digite o número do serviço (1 a 4)
ou digite *menu* para voltar ao menu principal.
""".strip()

SERVICOS_DETALHES = {
    "1": (
        "✅ *Biodescontaminação assistida e certificada*\n\n"
        "É o carro-chefe da empresa. Responsável por descontaminar ambientes seguindo diversas etapas.\n"
        "1) Anamnese ambiental\n"
        "2) Planejamento e preparação\n"
        "3) Execução técnica conforme protocolo\n"
        "4) Validação e certificação\n\n"
  "Digite *menu* para ver a lista de serviços novamente ou *menu* para voltar ao menu principal."
    ),
    "2": (
        "✅ *SASMUV*\n\n"
        "Serviço de controle de vetores e pragas, com aplicação técnica para reduzir a proliferação de mosquitos.\n"
        "É uma solução móvel e ágil, inspirada no conceito do fumacê, aplicada com critérios de segurança.\n\n"
        "Digite *menu* para ver a lista de serviços novamente ou *menu* para voltar ao menu principal."
 ),
    "3": (
        "✅ *Banho no leito*\n\n"
        "Serviço voltado a pacientes acamados, buscando mais conforto, higiene e qualidade no cuidado.\n"
        "Ajuda a melhorar o bem-estar e a experiência do paciente no ambiente hospitalar.\n\n"
        "Digite *menu* para ver a lista de serviços novamente ou *menu* para voltar ao menu principal."
    ),
    "4": (
        "✅ *Saúde Mental*\n\n"
        "Serviço de apoio em saúde mental para empresas e equipes, com foco em bem-estar, prevenção e suporte.\n"
        "Indicado para organizações que desejam cuidar melhor do clima, produtividade e saúde emocional.\n\n"
        "Digite *menu* para ver a lista de serviços novamente ou *menu* para voltar ao menu principal."
    ),
}

# ----------------------------
# 2) Estado (memória) por usuário
# ----------------------------
# Em produção, isso deve ser persistido (ex: Supabase)
user_state = {}  # exemplo: {"whatsapp:+5561999999999": "SERVICOS"}

# ----------------------------
# 3) Helpers
# ----------------------------

def twiml_message(texto: str) -> Response:
    """Gera resposta TwiML (XML) para o Twilio com a mensagem dada."""
    root = ET.Element("Response")
    msg = ET.SubElement(root, "Message")
    msg.text = texto

    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    xml_completo = '<?xml version="1.0" encoding="UTF-8"?>' + xml_str
    return Response(xml_completo, mimetype="application/xml")


def responder(body: str, from_number: str) -> str:
    """
    Decide a resposta com base no texto do usuário e no estado atual.
    """
    texto = (body or "").strip()
    texto_lower = texto.lower()

    # 3.1) Comandos globais (sempre funcionam)
    if texto_lower in ("menu", "opções", "opcoes", "voltar", "0"):
        user_state.pop(from_number, None)  # limpa estado do usuário
        return MENU

    if texto_lower in ("oi", "ola", "olá", "bom dia", "boa tarde", "boa noite", "hello"):
        user_state.pop(from_number, None)
        return MENU

    # 3.2) Se o usuário está dentro do submenu de serviços
    if user_state.get(from_number) == "SERVICOS":
        # Se ele digitar 1/2/3/4 -> mostra detalhe do serviço
        if texto in SERVICOS_DETALHES:
            return SERVICOS_DETALHES[texto]

        return f"Opção *{texto}* inválida.\n\n{SERVICOS_MENU}"

    # 3.3) Menu principal (fora do submenu)
    if texto == "4":
        # Entra no submenu de serviços
        user_state[from_number] = "SERVICOS"
        return SERVICOS_MENU

    if texto in OPCOES_MENU_PRINCIPAL:
        return OPCOES_MENU_PRINCIPAL[texto]

    # 3.4) Não reconhecido
    return f"Opção *{texto}* não encontrada.\n\n{MENU}"


# ----------------------------
# 4) Rotas Flask
# ----------------------------

@app.route("/webhook/whatsapp", methods=["POST"])
def webhook_whatsapp():
    """Recebe mensagens do Twilio (WhatsApp) e responde."""
    body = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "").strip()  # ex: "whatsapp:+55..."
    logger.info("Webhook chamado! From=%r Body=%r", from_number, body)

    resposta_texto = responder(body, from_number) if body else MENU
    return twiml_message(resposta_texto)


@app.route("/", methods=["GET"])
def health():
    """Para checar se o servidor está no ar."""
    return "Chatbot WhatsApp ativo."


# ----------------------------
# 5) Start local
# ----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)