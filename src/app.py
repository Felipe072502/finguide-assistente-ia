import json
import os
import re
import unicodedata
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODELO_PADRAO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

ARQUIVOS_BASE = [
    "orcamento.json",
    "credito.json",
    "dividas.json",
    "planejamento.json",
    "seguranca.json",
    "faq.json",
]

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "e", "em", "no", "na",
    "nos", "nas", "para", "por", "com", "sem", "que", "qual",
    "quais", "como", "me", "meu", "minha", "eu", "voce", "voces",
    "isso", "isto", "ser", "ter", "tem", "tenho", "quero",
}


# ============================================================
# BASE DE CONHECIMENTO
# ============================================================

def normalizar(texto: str) -> str:
    """Remove acentos e deixa o texto em minúsculas."""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return texto.lower()


def tokenizar(texto: str) -> list[str]:
    """Transforma o texto em palavras úteis para a busca."""
    palavras = re.findall(r"[a-zA-ZÀ-ÿ0-9]+", normalizar(texto))

    return [
        palavra
        for palavra in palavras
        if len(palavra) > 1 and palavra not in STOPWORDS
    ]


@st.cache_data
def carregar_base() -> list[dict]:
    """Carrega os registros JSON e identifica arquivo e tema de origem."""
    registros = []

    for nome_arquivo in ARQUIVOS_BASE:
        caminho = DATA_DIR / nome_arquivo

        if not caminho.exists():
            continue

        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        for item in dados.get("itens", []):
            registro = dict(item)
            registro["_arquivo"] = nome_arquivo
            registro["_tema"] = dados.get("tema", "")
            registros.append(registro)

    return registros


def texto_registro(registro: dict) -> str:
    """Converte um registro inteiro em texto pesquisável."""
    partes = []

    for chave, valor in registro.items():
        if chave.startswith("_"):
            continue

        if isinstance(valor, list):
            partes.extend(str(item) for item in valor)

        elif isinstance(valor, dict):
            partes.extend(
                f"{chave_interna} {valor_interno}"
                for chave_interna, valor_interno in valor.items()
            )

        else:
            partes.append(str(valor))

    return " ".join(partes)


def pontuar_registro(pergunta: str, registro: dict) -> int:
    """Calcula uma pontuação simples de relevância."""
    pergunta_normalizada = normalizar(pergunta)
    tokens = tokenizar(pergunta)

    titulo = normalizar(
        str(registro.get("titulo", registro.get("pergunta", "")))
    )

    palavras_chave = [
        normalizar(str(palavra))
        for palavra in registro.get("palavras_chave", [])
    ]

    texto = normalizar(texto_registro(registro))

    score = 0

    for token in tokens:
        if token in titulo:
            score += 4

        if any(token in palavra for palavra in palavras_chave):
            score += 3

        if token in texto:
            score += 1

    if pergunta_normalizada and pergunta_normalizada in texto:
        score += 5

    for palavra in palavras_chave:
        if palavra and palavra in pergunta_normalizada:
            score += 6

    return score


def buscar_contexto(pergunta: str, limite: int = 4) -> list[dict]:
    """Recupera os registros mais relacionados à pergunta."""
    pontuados = []

    for registro in carregar_base():
        score = pontuar_registro(pergunta, registro)

        if score > 0:
            pontuados.append((score, registro))

    pontuados.sort(key=lambda item: item[0], reverse=True)

    return [
        registro
        for _, registro in pontuados[:limite]
    ]


def contexto_para_prompt(registros: list[dict]) -> str:
    """Monta o contexto que será enviado para a IA."""
    if not registros:
        return (
            "Nenhum conteúdo relevante foi encontrado na base de conhecimento. "
            "Não invente informações. Se a pergunta estiver dentro do escopo, "
            "explique que a base não possui informação suficiente."
        )

    blocos = []

    for registro in registros:
        conteudo = {
            chave: valor
            for chave, valor in registro.items()
            if not chave.startswith("_")
        }

        blocos.append(
            f"TEMA: {registro.get('_tema', '')}\n"
            f"ARQUIVO: {registro.get('_arquivo', '')}\n"
            f"DADOS:\n"
            f"{json.dumps(conteudo, ensure_ascii=False, indent=2)}"
        )

    return "\n\n---\n\n".join(blocos)


# ============================================================
# GEMINI API
# ============================================================

def perguntar_gemini(
    pergunta: str,
    contexto: str,
    modelo: str,
) -> str:
    """Envia o contexto e a pergunta para a Gemini API."""
    if not GEMINI_API_KEY:
        return (
            "A chave da Gemini API ainda não foi configurada. "
            "Crie um arquivo .env na raiz do projeto e adicione "
            "GEMINI_API_KEY=sua_chave."
        )

    mensagem_usuario = f"""
CONTEXTO RECUPERADO DA BASE DE CONHECIMENTO:

{contexto}

PERGUNTA DO USUÁRIO:

{pergunta}

Responda respeitando rigorosamente as regras do FinGuide.
"""

    try:
        cliente = genai.Client(api_key=GEMINI_API_KEY)

        resposta = cliente.models.generate_content(
            model=modelo,
            contents=mensagem_usuario,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1200,
            ),
        )

        texto = (resposta.text or "").strip()

        if not texto:
            return (
                "A API não retornou uma resposta em texto. "
                "Tente novamente ou confira o modelo configurado."
            )

        return texto

    except Exception as erro:
        return (
            "Não foi possível consultar a Gemini API. "
            "Confira sua chave, conexão com a internet, cota da API "
            "e o nome do modelo configurado.\n\n"
            f"Detalhe técnico: {erro}"
        )


# ============================================================
# INTERFACE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="FinGuide",
    page_icon="💰",
    layout="centered",
)

st.title("💰 FinGuide")
st.subheader("Assistente Virtual de Educação Financeira")

st.caption(
    "Protótipo educacional desenvolvido para o desafio "
    "\"Construa Seu Assistente Virtual Com Inteligência Artificial\"."
)

with st.sidebar:
    st.header("⚙️ Configurações")

    modelo = st.text_input(
        "Modelo Gemini",
        value=MODELO_PADRAO,
        help="Modelo padrão do projeto: gemini-3.5-flash-lite",
    )

    mostrar_contexto = st.checkbox(
        "Mostrar contexto recuperado",
        value=False,
        help=(
            "Exibe quais registros da base foram enviados "
            "como contexto para a IA."
        ),
    )

    if GEMINI_API_KEY:
        st.success("Gemini API configurada.")
    else:
        st.error(
            "GEMINI_API_KEY não configurada. "
            "Copie .env.example para .env e informe sua chave."
        )

    st.divider()

    st.markdown(
        """
        **O FinGuide pode ajudar com:**

        - orçamento pessoal;
        - crédito e juros;
        - dívidas;
        - planejamento financeiro;
        - segurança financeira.
        """
    )

    st.warning(
        "O FinGuide possui finalidade educacional. "
        "Ele não realiza operações bancárias nem substitui "
        "orientação profissional."
    )

    if st.button("Limpar conversa"):
        st.session_state.messages = []
        st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(
            "Olá! Eu sou o **FinGuide**. Posso ajudar você a entender "
            "conceitos de educação financeira. O que você gostaria de saber?"
        )


for mensagem in st.session_state.messages:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])


pergunta = st.chat_input(
    "Ex.: O que é CET? / É melhor pagar à vista ou parcelar?"
)

if pergunta:
    st.session_state.messages.append({
        "role": "user",
        "content": pergunta,
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    registros = buscar_contexto(pergunta)
    contexto = contexto_para_prompt(registros)

    with st.chat_message("assistant"):
        with st.spinner("Consultando a base e a Gemini API..."):
            resposta = perguntar_gemini(
                pergunta=pergunta,
                contexto=contexto,
                modelo=modelo,
            )

        st.markdown(resposta)

        if mostrar_contexto:
            with st.expander("🔎 Contexto usado na resposta"):
                if registros:
                    for registro in registros:
                        titulo = registro.get(
                            "titulo",
                            registro.get("pergunta", "Registro"),
                        )

                        st.markdown(
                            f"**{titulo}**  \n"
                            f"`{registro.get('_arquivo', '')}`"
                        )

                else:
                    st.info(
                        "Nenhum registro relevante foi encontrado na base."
                    )

                st.code(contexto, language="text")

    st.session_state.messages.append({
        "role": "assistant",
        "content": resposta,
    })
