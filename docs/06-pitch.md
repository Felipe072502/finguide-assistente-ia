# 06 — Pitch Final do FinGuide

## Versão curta — aproximadamente 2 minutos

Olá! Este projeto se chama **FinGuide** e foi desenvolvido para o desafio **Construa Seu Assistente Virtual Com Inteligência Artificial**, do Bootcamp Bradesco na DIO.

A proposta surgiu de um problema comum: muitas pessoas precisam tomar decisões financeiras no dia a dia, mas nem sempre entendem conceitos como juros, CET, crédito, endividamento, reserva financeira ou custo de uma operação.

O FinGuide é um assistente virtual de educação financeira criado para tornar esses conceitos mais simples e acessíveis.

A pessoa usuária faz uma pergunta em linguagem natural, como:

- “O que é CET?”
- “É melhor pagar à vista ou parcelar?”
- “Como funcionam os juros compostos?”
- “Pediram um Pix antes de liberar um empréstimo. Isso é seguro?”

Antes de gerar uma resposta, a aplicação procura informações relevantes em uma base de conhecimento local organizada em arquivos JSON.

Essa base possui conteúdos sobre orçamento, crédito, juros, dívidas, planejamento financeiro e segurança.

Os registros encontrados são enviados para o modelo de linguagem junto com um conjunto de regras que define como o FinGuide deve se comportar.

Um dos principais pontos do projeto é a estratégia contra alucinação.

O assistente foi instruído a não inventar taxas, valores ou condições financeiras. Quando não possui informação suficiente, ele deve informar isso claramente.

Além disso, o FinGuide não recomenda a compra ou venda de ativos específicos, não garante aprovação de crédito e não toma decisões pelo usuário.

A aplicação foi desenvolvida em Python com Streamlit e utiliza a Gemini API para gerar as respostas.

Também foram criados 15 cenários de teste para avaliar o comportamento do assistente em critérios como assertividade, fundamentação, segurança, clareza e aderência ao escopo.

Os resultados finais serão registrados somente após a execução real desses testes.

O principal aprendizado deste projeto foi entender que a qualidade de um assistente de IA não depende apenas do modelo utilizado.

A organização da base de conhecimento, a recuperação de contexto, a construção do prompt e os testes são fundamentais para produzir respostas mais confiáveis.

Como evolução futura, o FinGuide poderia utilizar busca vetorial com embeddings, fontes oficiais atualizadas e citações das informações usadas em cada resposta.

Obrigado!


---

# Roteiro detalhado — aproximadamente 3 minutos

## 1. Problema

Muitas pessoas lidam diariamente com situações como cartão de crédito, empréstimos, parcelamentos e organização do orçamento.

Mesmo assim, conceitos como juros, CET, custo total de uma dívida ou reserva de emergência nem sempre são fáceis de entender.

Além disso, uma resposta financeira ruim pode causar confusão quando apresenta informações sem contexto ou dados inventados.

## 2. Solução

O FinGuide foi criado como um assistente virtual de educação financeira.

Seu objetivo é ajudar a pessoa usuária a compreender conceitos financeiros e organizar os fatores envolvidos em uma decisão.

Ele pode responder perguntas sobre:

- orçamento;
- crédito;
- juros;
- dívidas;
- planejamento financeiro;
- segurança financeira.

## 3. Funcionamento

O fluxo da aplicação é simples:

```text
Usuário
   ↓
Pergunta no chatbot
   ↓
Busca na base de conhecimento
   ↓
Recuperação dos conteúdos relevantes
   ↓
Prompt + contexto
   ↓
Modelo de linguagem
   ↓
Resposta do FinGuide
```

A base de conhecimento foi organizada em arquivos JSON.

A recuperação é feita por palavras-chave, permitindo que o sistema selecione apenas os conteúdos mais relacionados à pergunta.

## 4. Inteligência Artificial

O modelo de linguagem recebe três elementos:

1. o System Prompt;
2. o contexto recuperado;
3. a pergunta do usuário.

O System Prompt define o comportamento do agente e inclui regras contra respostas inventadas.

## 5. Segurança e anti-alucinação

O FinGuide não deve:

- inventar taxas de juros;
- criar valores financeiros;
- garantir aprovação de crédito;
- garantir resultados;
- recomendar ativos específicos;
- responder como se tivesse dados atuais quando não possui uma fonte atualizada.

Quando faltam dados, o assistente deve informar essa limitação.

## 6. Aplicação

A interface foi construída com Streamlit.

O usuário conversa com o FinGuide por meio de um chat.

Existe também uma opção para mostrar o contexto recuperado da base, permitindo visualizar quais informações foram utilizadas na resposta.

Essa funcionalidade ajuda tanto na demonstração quanto nos testes.

## 7. Avaliação

Foram definidos 15 cenários de teste.

Eles incluem perguntas normais e situações de borda, como:

- tentativa de prompt injection;
- solicitação de taxa atual;
- recomendação de ações;
- perguntas fora do escopo;
- possível golpe financeiro.

Cada resposta é avaliada em cinco critérios:

- assertividade;
- fundamentação;
- segurança;
- clareza;
- aderência ao escopo.

Os resultados só serão publicados depois que os testes forem realmente executados.

## 8. Aprendizados

O maior aprendizado do projeto foi perceber que criar um assistente de IA envolve mais do que apenas chamar um modelo.

Também é necessário:

- organizar o conhecimento;
- recuperar o contexto correto;
- definir limites;
- criar prompts claros;
- testar respostas;
- medir comportamento.

## 9. Próximos passos

Como melhorias futuras, o projeto poderia incluir:

- embeddings;
- banco vetorial;
- recuperação semântica;
- fontes oficiais atualizadas;
- referências nas respostas;
- histórico de conversa mais avançado;
- painel de avaliação.


---

## Pitch em uma frase

**FinGuide é um assistente virtual de educação financeira que usa uma base de conhecimento controlada e regras anti-alucinação para explicar orçamento, crédito, juros, dívidas, planejamento e segurança de forma simples e transparente.**

