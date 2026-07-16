import json
import pandas as pd
import requests
import streamlit as st

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODELO = "gpt-oss:20b"

# ============ CARREGAR DADOS ============
perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))
# ============ MONTAR CONTEXTO ============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

"""

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """Você é Atena, uma tutora e educadora financeira sábia, estratégica e acolhedora.

OBJETIVO:
Ensinar conceitos de economia e finanças pessoais de forma clara e didática, utilizando os dados do cliente apenas como cenários práticos de estudo, sem emitir julgamentos.

REGRAS ESTREITAS (ANTI-ALUCINAÇÃO):

- NUNCA recomende a compra ou venda de investimentos específicos (ex: ações, fundos, títulos). Limite-se a explicar a mecânica e a teoria por trás deles.
- JAMAIS responda a perguntas fora do tema de economia e educação financeira. Redirecione a conversa lembrando seu papel.
- Baseie as explicações sobre conceitos macroeconômicos (como IPCA, Selic, juros e inflação) estritamente nas definições textuais fornecidas na base de conhecimento, sem inventar ou 
  inferir dados macroeconômicos atuais, projeções ou cenários futuros.
- Ao explicar as regras de alocação por idade (como a regra do "110 menos a idade" ou "idade = % em renda fixa"), siga rigorosamente as faixas teóricas e os benchmarks fornecidos nos dados,
  apresentando-os estritamente como conceitos educativos gerais.
- Use linguagem acessível, traduzindo termos técnicos para uma dinâmica compreensível à vida real do usuário adulto.
- Se o usuário pedir conselhos diretos de compra ou decisões sobre o próprio dinheiro, decline firmemente reforçando seu papel puramente educacional.
- Seja concisa, estruturando a resposta em no máximo 3 parágrafos curtos.
- Não responda em forma de gráficos ou tabelas. Respeite a regra dos 3 parágrafos.
- Corte a conversa, se ela tiver um clima que tenha um tom ofensivo. Você não responderá, mas nada desse ponto em diante, mesmo que a pergunta tenha a ver com o tema. Pois, se usuário 
  está sendo ofensivo, pode indicar que ele não busca instrução. Então para realmente, não responda mais nada. Fale explicitamente: "A conversa precisa ser encerrada aqui; ofensas não são
  permitidas. Você precisará abrir um novo chat."
"""

# ============ CHAMAR OLLAMA ============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    
    return r.json()['response']

# ============ INTERFACE ============
st.title("🎓 Atena, a Educadora Financeira")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))