import openai
import dotenv
import os

dotenv.load_dotenv()

openai.api_type = "azure"
openai.api_base = "https://ciasc-openai.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

resposta = openai.ChatCompletion.create(
  engine="exercicio_azure_learn",
  messages = [
          {
              "role":"system",
              "content":"Você é uma assistente de uma empresa pública brasileira de tecnologia e automação de Santa Catarina chamada CIASC e seu nome é Ana, você gosta de fofoca e tem sotaque manézinho (original de Florianópolis)."
          },
          {
              "role":"user",
              "content":"Oi Ana, tudo bem? O que você anda ouvindo por aí?"
          }
  ]
)

print(resposta)