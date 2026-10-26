# Mini-SOC com Inteligência Artificial

## 📌 Sobre o Projeto
Este projeto simula a operação de um SOC (Security Operations Center) moderno, utilizando Inteligência Artificial para automatizar a análise de logs de segurança. O objetivo é reduzir o tempo de resposta a incidentes e a fadiga do analista, que não precisa ler milhares de linhas manualmente.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **Google Gemini API** (Modelo `gemini-3.6-flash` via `google-genai` SDK)
* **Linux** (Análise de logs de autenticação `/var/log/auth.log`)

## ⚙️ Como Funciona
1. O script lê um arquivo de log de autenticação (`auth.log`).
2. Ele filtra apenas as linhas que indicam falha de login (`Failed password`).
3. Esses dados são enviados para a API do Google Gemini com um prompt de "Analista Sênior de SOC".
4. A IA analisa os padrões, identifica se é um ataque de força bruta, aponta o IP do atacante e sugere medidas de mitigação.
5. O resultado é exibido no terminal e salvo em um arquivo `relatorio_incidente.md`.

## 🚧 Desafios Técnicos e Soluções (O Diferencial)
Durante o desenvolvimento, o projeto enfrentou instabilidades comuns em ambientes de nuvem:
* **Modelos Descontinuados:** A API do Google desativou modelos antigos (como o `gemini-2.5-flash` e `1.5-flash`) para novas contas.
* **Indisponibilidade (Erro 503):** O servidor do modelo `gemini-3.8-flash` apresentou instabilidade (Service Unavailable) durante os testes, conforme evidenciado pelos gráficos de uso do Google AI Studio.
* **Solução Implementada:** Foi implementado um mecanismo de **Retry (tentativa automática)** com backoff, além da migração para o modelo `gemini-3.6-flash`, que apresenta maior estabilidade para chaves gratuitas. O código trata o erro 503 de forma amigável, aguardando e tentando novamente, garantindo a resiliência da aplicação.

## 🚀 Como Executar
1. Clone o repositório.
2. Crie um ambiente virtual: `python3 -m venv venv`
3. Ative o ambiente: `source venv/bin/activate`
4. Instale as dependências: `pip install google-genai python-dotenv`
5. Crie um arquivo `.env` com a sua `GEMINI_API_KEY`.
6. Execute: `python soc_ia.py`
