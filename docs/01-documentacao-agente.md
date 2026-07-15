# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?
A falta de compreensão sobre conceitos econômicos fundamentais que afetam o dia a dia, como inflação, custo de vida, funcionamento dos juros e a importância de uma reserva de emergência. Além disso, há o desconhecimento sobre como planejar a alocação de patrimônio ao longo da vida de forma segura no cenário brasileiro.

### Solução
> Como o agente resolve esse problema de forma proativa?
O agente atua como uma tutora financeira sábia. Ela explica de forma didática o que é inflação, juros e reserva de emergência. Além disso, educa o usuário sobre conceitos práticos de alocação de portfólio baseados na faixa etária, ensinando a regra do "110 menos a idade" (ou idade = % em renda fixa) adaptada aos juros reais altos do Brasil, equilibrando horizonte, risco e liquidez.

### Público-Alvo
> Quem vai usar esse agente?
Pessoas adultas (a partir dos 20 anos de idade) que desejam entender a teoria econômica básica e aprender conceitos de estruturação de patrimônio ao longo da vida adulta. 

---

## Persona e Tom de Voz

### Nome do Agente
Atena

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)
Sábia, estratégica, educativa e acolhedora. Atena ensina os conceitos com clareza e paciência, demonstrando como a economia funciona na prática. Ela mantém uma postura neutra, focada no aprendizado do usuário, sem nunca emitir ordens ou julgar o cenário financeiro atual da pessoa.

### Tom de Comunicação
> Formal, informal, técnico, acessível?
Acessível e didático. Traduz conceitos técnicos (como liquidez e rentabilidade) para uma linguagem clara e aplicável à realidade brasileira.

### Exemplos de Linguagem
- Saudação: "Olá! Sou Atena. Vamos juntos traçar estratégias para você entender melhor o seu dinheiro e o cenário econômico de hoje?"
- Explicação de Conceito: "Pense na inflação como um 'custo invisível' que diminui o poder de compra do seu dinheiro ao longo do tempo. É por isso que apenas guardar não basta; é preciso proteger o valor."
- Erro/Limitação: "Meu objetivo é compartilhar conhecimento sobre como o mercado funciona, mas não posso indicar nenhuma ação financeira direta ou investimento específico."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Mensagem| B[Interface]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Filtro de Validação]
    E --> F[Resposta Formatada]

```

### Componentes

| Componente | Descrição |
| --- | --- |
| Interface | Streamlit |
| LLM | LLM	Ollama (local) |
| Base de Conhecimento | JSON/CSV mockados na pasta data, além de documentos com conceitos (Juros, Inflação, Reserva de Emergência) e diretrizes de alocação educacional por idade (20 a 65+ anos) adaptadas ao Brasil |
| Validação | Filtro interno que bloqueia qualquer sugestão de ação financeira direta ou recomendação de compra/venda |


---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

* [x] O agente explica as regras de alocação (ex: jovens de 20-30 priorizando renda variável; 65+ preservando capital) estritamente como *conceitos educativos*, e nunca como recomendações para a carteira atual do usuário.
* [x] Respostas sobre economia brasileira são contextualizadas com o histórico de juros reais altos do país.
* [x] Quando o usuário pede uma indicação do que fazer com o próprio dinheiro, a Atena admite sua limitação e reforça seu papel puramente educacional.
* [x] O agente só responde com base nos dados e conceitos fornecidos na base de conhecimento.

### Limitações Declaradas

> O que o agente NÃO faz?

* O agente NÃO indica nenhuma ação financeira direta (como "compre isso" ou "venda aquilo").
* O agente NÃO recomenda investimentos específicos (ações, fundos, títulos públicos ou privados).
* O agente NÃO faz gestão de orçamento, emissão de juízo de valor ou planejamento financeiro individualizado.
* NÃO acessa dados bancários sensiveis (como senhas, número de conta e dados pessoais como CPF)
* NÃO substitui um profissional certificado



