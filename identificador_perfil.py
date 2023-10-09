import openai
import os
import dotenv
import tiktoken
import time

dotenv.load_dotenv()

openai.api_type = "azure"
openai.api_base = "https://ciasc-openai.openai.azure.com/" #max tokens = 4096
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def identificaPerfil(prompt_usuario, prompt_sistema, nro_relatorio):
    
    # ==================== VERIFICA QUAL MODELO DEVE SER USADO ====================
    eng = "ia_ciasc"  #modelo gpt-3.5-turbo
    tam_esperado_saida = 2048
    tentativa = 0
    tempo_de_tentativa = 5
    
    codificador = tiktoken.encoding_for_model("gpt-3.5-turbo")
    lista_tokens = codificador.encode(prompt_usuario + prompt_sistema)
    nro_tokens = len(lista_tokens)
    print(f"Número de tokens de entrada:{nro_tokens}")

    if nro_tokens >= 4096 - tam_esperado_saida:
      eng = "ia_ciasc_16k" #modelo gpt-3.5-turbo-16k
    print(f"Implementação escolhida: {eng}")
    # ==================== FIM DA VERIFICAÇÃO ====================

    # ================ USA REQUISIÇÃO ========================
    while tentativa <= 3:
        tentativa += 1
        try: 
            resposta = openai.ChatCompletion.create(
            engine=eng,
            messages=[
                {
                "role": "system",
                "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ],
            temperature=1.3,
            max_tokens=8000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            )
            salva(f"./dados/{nro_relatorio}-relatorio2-otakus", resposta.choices[0].message.content)
            print("Relatório criado com sucesso!")
            return
        # Tratamento de ERROS:
        except openai.error.AuthenticationError as e:
            print("Erro de Autenticação:", e)
        except openai.error.APIError as e:
            print("Erro de API:", e)
            if tentativa != 3:
                print("Aguarde. Tentando requisição novamente...")
            time.sleep(15)
        except openai.error.RateLimitError as e:
            print("Erro de taxa limite de requisição:", e)
            tempo_de_tentativa *= 2 #tecnica usada para não exagerar nas requisições
      


    # ======================= TERMINA REQUISIÇÃO =======================
prompt_sistema = f"""
    Você é um analisador de gostos e recomendador de animes.
    - Identifique o gosto de consumo de animes para cada pessoa da tabela a seguir. Cada linha se refere a uma pessoa. 
    - Recomende 3 animes baseando-se na preferência dela e na lista de animes que a pessoa tem como favoritos. 
    - A lista de favoritos de cada pessoa se encontra em ordem decrescente de gosto(1º lugar podendo chegar até o 10º lugar).
    - JAMAIS recomende animes que já estão presentes na lista de animes da pessoa. 
    - Considere que a pessoa pode ter escrito de maneira equivocada o título do anime.
    - Não recomende continuações de animes, por exemplo: Naruto Shippuden caso a pessoa goste de Naruto.
    - Não recomende filmes de continuação ou de história paralela de um anime compostos de episódios. Por exemplo: One Piece: Z, Dragon Ball Brolly, etc...
    - A recomendação pode ser tanto animes compostos por episódios quanto filmes.

    ####Formato de saída deve ser apenas:

    Nick: [nickname da pessoa]
    Animes Recomendados:
    1. [anime recomendado 1]
    2. [anime recomendado 2]
    3. [anime recomendado 3]
    Justificativa:[Motivo pelo qual estas 3 recomendações acima são boas para a pessoa. No máximo 20 palavras.]
    Genêro Favorito:[A resposta deve ser um desses: SHOUJO, SEINEN, SHOUNEN, ISEKAI, ECCHI, HENTAI, JOSEI, KODOMO, HAREM, SLICE OF LIFE, MECHA, KEMONO ou MAHOU SHOUJO]
    """
# =========== COMEÇO DO PROGRAMA =============

print("Gostaria de analisar como? \n 1. Apenas um arquivo \n 2. Varios arquivos \n 3. Sair")
escolha = int(input("Digite sua escolha: "))

while escolha > 2 or escolha < 0:
    print("escolha entre as opções 1, 2 ou 0")
    escolha = int(input("Digite sua escolha: "))

    #TESTES INDIVIDUAIS
if escolha == 1:
    print("Qual arquivo gostaria? \n 0 - Todos \n 1 a 11 - Grupo [sua escolha] ")
    escolha_arq = int(input("Resposta: "))
    if escolha_arq > 0 and escolha_arq <= 11:
        arquivo = f"./dados/dados_grupo{escolha_arq}.csv"
    elif escolha_arq == 0:
        arquivo = f"./dados/dados_otakus.csv"
    else:
        print("Escolha corretamente")
    prompt_user = carrega(arquivo)
    identificaPerfil(prompt_user, prompt_sistema, escolha_arq)

    #TESTES COM GRUPOS DE ARQUIVOS
elif escolha == 2:
    lista_arquivos = []
    print("Escolha os arquivos de 1 a 11. Quando quiser parar de adicionar, selecione 0: ")
    print("")
    escolha_arq = int(input("Adicione um arquivo: "))
    while escolha_arq != 0:
        if f"./dados/dados_grupo{escolha_arq}.csv" in lista_arquivos:
            print(escolha_arq, "Já existe esse arquivo na lista")
        else:
            lista_arquivos.append(f"./dados/dados_grupo{escolha_arq}.csv")
            print("Arquivo",escolha_arq,"adicionado a lista")
        escolha_arq = int(input("Adicione um arquivo: "))
    print(lista_arquivos)
    for nome_do_arquivo in lista_arquivos:
        prompt_user = carrega(nome_do_arquivo)
        identificaPerfil(prompt_user, prompt_sistema, (lista_arquivos.index(nome_do_arquivo)+1))

elif escolha == 0:
    print("ok, tchau!")

