import openai
import dotenv
import os

dotenv.load_dotenv()

openai.api_type = "azure"
openai.api_base = "https://ciasc-openai.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

def categorizaAnime(nome_do_anime, generos_validos):
    prompt_sistema = f"""
    Você é um categorizador de animes.
    Você deve escolher um gênero da lista abaixo:
    Se os gêneros informadas não forem gêneros válidos, responda com "Não posso ajudá-lo com isso"
    ##### Lista de gêneros válidos
    {generos_validos}
    ##### Exemplo
    One Piece
    Shounen
    """
    resposta = openai.ChatCompletion.create(
    engine="exercicio_azure_learn",
    messages=[
        {
        "role": "system",
        "content": prompt_sistema
        },
        {
            "role": "user",
            "content": nome_do_anime
        }
    ],
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    )
    print(resposta.choices[0].message.content)

print("Digite as categorias validas:")
generos_validos = input()
while True:
    print("Digite o nome do produto:")
    nome_do_anime = input()
    categorizaAnime(nome_do_anime, generos_validos)