# 04 — Aplicação Funcional

## Objetivo

O FinGuide possui uma aplicação de chat desenvolvida em Python com Streamlit.

O protótipo conecta:

1. interface de conversa;
2. base de conhecimento em JSON;
3. Gemini API como modelo de linguagem externo.

## Fluxo

```text
Usuário
   ↓
Pergunta no Streamlit
   ↓
Busca por palavras-chave
   ↓
Registros relevantes da base
   ↓
Contexto + System Prompt
   ↓
Gemini API
   ↓
Resposta do FinGuide
```

## Por que usar uma API externa?

A geração acontece na infraestrutura do provedor da API. Assim, o computador local executa apenas Python, Streamlit e a recuperação da base de conhecimento.

Isso reduz a necessidade de memória RAM e de GPU em comparação com a execução de um modelo de linguagem local.

## Modelo padrão

```text
gemini-2.5-flash
```

O modelo pode ser alterado pela variável `GEMINI_MODEL` ou na barra lateral da aplicação.

## Configuração da chave

A chave nunca deve ser colocada diretamente no código.

Crie um arquivo `.env` na raiz do projeto usando `.env.example` como referência:

```env
GEMINI_API_KEY=sua_chave
GEMINI_MODEL=gemini-2.5-flash
```

O arquivo `.env` está incluído no `.gitignore` e não deve ser enviado ao GitHub.

## Como executar

### 1. Criar o ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar a Gemini API

Copie:

```text
.env.example
```

para:

```text
.env
```

e preencha sua chave.

### 4. Executar

```bash
streamlit run src/app.py
```

## Transparência

A opção **Mostrar contexto recuperado** permite visualizar quais registros da base foram enviados à API. Isso facilita testes, demonstração do projeto e investigação de possíveis alucinações.

## Segurança da chave

Nunca:

- coloque a chave diretamente no `app.py`;
- envie o arquivo `.env` para o GitHub;
- publique a chave em prints ou documentação;
- compartilhe a chave em commits.

Se uma chave for exposta, ela deve ser revogada e substituída.
