import openai
import os
import dotenv
import tiktoken

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

def identificaPerfil(prompt_usuario, prompt_sistema):
    
    # ==================== VERIFICA QUAL MODELO DEVE SER USADO ====================
    eng = "ia_ciasc"  #modelo gpt-3.5-turbo
    tam_esperado_saida = 2048
    
    codificador = tiktoken.encoding_for_model("gpt-3.5-turbo")
    lista_tokens = codificador.encode(prompt_usuario + prompt_sistema)
    nro_tokens = len(lista_tokens)
    print(f"Número de tokens de entrada:{nro_tokens}")

    if nro_tokens >= 4096 - tam_esperado_saida:
      eng = "ia_ciasc_16k" #modelo gpt-3.5-turbo-16k
    print(f"Implementação escolhida: {eng}")
    # ==================== FIM DA VERIFICAÇÃO ====================

    # ================ USA REQUISIÇÃO ========================
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
    temperature=1,
    max_tokens=tam_esperado_saida,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    )
    print(resposta.choices[0].message.content)
    # ======================= TERMINA REQUISIÇÃO =======================
prompt_sistema = f"""
    Você é um recomendador de animes.
    - Identifique o perfil de consumo de animes para cada pessoa da tabela a seguir. 
    - Recomende 3 animes baseando-se no perfil e na lista de animes que a pessoa tem como favoritos. 
    - A lista de favoritos de cada pessoa se encontra em ordem decrescente de gosto.
    - Considere que a pessoa pode ter escrito de maneira equivocada o título do anime.
    - Não recomende animes que já estão presentes na lista de animes favoritos da pessoa, pois ela já assistiu. 
    - Não recomende continuações de animes, por exemplo: Naruto Shippuden caso a pessoa goste de Naruto.
    - Não recomende filmes de continuação ou de história paralela de um anime compostos de episódios. Por exemplo: One Piece: Z, Dragon Ball Brolly, etc...
    - A recomendação pode ser tanto animes compostos por episódios quanto filmes.

    O formato de saída deve ser apenas:

    nickname da pessoa
    1. anime recomendado 1
    2. anime recomendado 2
    3. anime recomendado 3
    """

primeiro_prompt = carrega("./dados/dados_otakus_tratados_22.csv")
identificaPerfil(primeiro_prompt, prompt_sistema)

