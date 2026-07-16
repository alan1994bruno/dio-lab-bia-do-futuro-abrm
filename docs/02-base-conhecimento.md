# Base de Conhecimento

## Dados Utilizados

A base de conhecimento da **Atena** foi expandida para suportar seu papel estritamente educacional. Abaixo estão os arquivos utilizados e suas respectivas funções:

| Arquivo                              | Formato | Para que serve na Atena?                                                                                                                                                      |
| ------------------------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `perfil_investidor.json`             | JSON    | Extrair a idade, renda e objetivos do usuário para personalizar o ensino (ex: aplicar a regra de alocação por idade baseada nos dados do perfil).                             |
| `historico_atendimento.csv`          | CSV     | Contextualizar dúvidas anteriores, garantindo fluidez no atendimento sem precisar repetir explicações básicas.                                                                |
| `investimento_fragmentado_idade.csv` | CSV     | Baseia as explicações sobre horizontes de investimento. Permite à Atena ensinar benchmarks de acúmulo e equilíbrio entre risco e liquidez conforme a fase da vida do usuário. |
| `produtos_financeiros.json`          | JSON    | Funciona como um "catálogo de estudos", e não de vendas. Serve para exemplificar as características de cada produto no cenário brasileiro, sem recomendar compra.             |

---

## Adaptações nos Dados

- Nas tentativas de rodar localmente, observaram-se anomalias ao aumentar a quantidade de informações, de modo que a IA começou a se perder nas respostas. Então, decidi usar apenas os dados mockados.

---

## Estratégia de Integração

### Como os dados são carregados?

A leitura dos arquivos ocorre no _backend_ via código (utilizando `pandas` para CSV e `json` nativo no Python) no momento em que a sessão é iniciada, isolando a base bruta do modelo de linguagem.

```python
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

```

###### Nota: Em testes locais, foi observado que colocar localhost, não está funcionando corretamente, foi colocado então o endereço IP manualmente e começou aparecer os logs no ollama server.

### Como os dados são usados no prompt?

Para otimizar o consumo de _tokens_ e garantir um foco preciso (anti-alucinação), a base de conhecimento bruta **não é injetada inteira** no prompt. O código processa e sintetiza as informações relevantes em formato de texto estruturado antes de enviá-las ao _System Prompt_.

---

## Exemplo de Contexto Montado

Abaixo está o exemplo real do _System Prompt_ gerado dinamicamente pelo código e enviado ao LLM. Note como os dados transacionais foram consolidados e a teoria de alocação por idade foi aplicada de forma puramente instrutiva:

```text
[INSTRUÇÕES DO SISTEMA]
Você é Atena, uma tutora financeira sábia.
Diretrizes: NÃO indique nenhuma ação financeira direta. Explique os conceitos adaptando-os à realidade brasileira.

[CONTEXTO DO CLIENTE]
- Nome: João Silva
- Idade: 32 anos
- Perfil: Moderado
- Renda Mensal: R$ 5.000,00
- Meta Principal: Construir reserva de emergência (Faltam R$ 5.000 para a meta de R$ 15.000).

[SÍNTESE DE GASTOS (MÊS ATUAL)]
- Moradia: R$ 1.380,00
- Alimentação: R$ 570,00
- Transporte: R$ 295,00
- Total de Saídas: R$ 2.488,90 (Aproximadamente 50% da renda).

[BASE DE CONHECIMENTO FILTRADA PARA A INTERAÇÃO]
- Diretriz de Idade (30-45 anos): Fase de equilibrar crescimento e proteção. A regra de referência sugere usar a própria idade (32) como percentual de base para Renda Fixa no Brasil, devido aos juros altos, e o restante em ativos de crescimento.
- Reserva de Emergência: Deve ficar em produtos de alta liquidez e baixo risco (exemplo didático: Tesouro Selic ou CDB de liquidez diária).

[MENSAGEM DO USUÁRIO]
"Atena, com base nos meus gastos, como eu poderia organizar minha alocação de investimentos agora que tenho 32 anos?"

```
