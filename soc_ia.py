import os
from google import genai
from dotenv import load_dotenv

# 1. Carrega a chave secreta do arquivo .env
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERRO: Chave da API não encontrada. Verifique o arquivo .env")
    exit(1)

# 2. Configura o novo cliente do Google GenAI
client = genai.Client(api_key=api_key)

# 3. Função para ler o log e extrair apenas as falhas
def ler_logs(caminho_arquivo):
    falhas = []
    try:
        with open(caminho_arquivo, 'r') as file:
            for linha in file:
                if "Failed password" in linha:
                    falhas.append(linha.strip())
        return falhas
    except FileNotFoundError:
        print(f"❌ ERRO: O arquivo {caminho_arquivo} não foi encontrado.")
        return []

# 4. Função principal
def main():
    print("🔍 Iniciando análise do SOC...")
    logs_suspeitos = ler_logs('auth.log')
    
    if not logs_suspeitos:
        print("✅ Nenhuma tentativa de login falha encontrada.")
        return

    print(f"⚠️ Encontradas {len(logs_suspeitos)} tentativas de login falhas.")
    print("🤖 Enviando dados para a Inteligência Artificial analisar...\n")

    # 5. Cria o prompt (a instrução) para a IA
    prompt = f"""
    Você é um analista de segurança sênior de um SOC (Security Operations Center).
    Analise os seguintes logs de autenticação de um servidor Linux e me forneça um relatório respondendo:
    1. Isso parece um ataque de força bruta? Qual é o endereço IP do atacante?
    2. Qual é a sua recomendação imediata de bloqueio?
    3. Escreva uma breve explicação técnica do que aconteceu.

    Aqui estão os logs:
    {chr(10).join(logs_suspeitos)}
    """

    # 6. Envia para a IA usando o novo SDK
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt
        )
        
        # 7. Exibe no terminal
        print("="*50)
        print("🚨 RELATÓRIO DO ANALISTA DE IA 🚨")
        print("="*50)
        print(response.text)
        
        # 8. Salva em um arquivo Markdown (para o portfólio)
        with open("relatorio_incidente.md", "w") as f:
            f.write("# Relatório de Incidente de Segurança\n\n")
            f.write(f"**Total de tentativas falhas analisadas:** {len(logs_suspeitos)}\n\n")
            f.write(response.text)
        print("\n✅ Relatório salvo com sucesso no arquivo 'relatorio_incidente.md'")

    except Exception as e:
        print(f"❌ Ocorreu um erro ao chamar a IA: {e}")

if __name__ == "__main__":
    main()
