import tiktoken

codificador = tiktoken.encoding_for_model("gpt-3.5-turbo")
lista_tokens = codificador.encode("Gostaria de saber sobre os produtos")
nro_tokens = len(lista_tokens)
valor = 0.0015
custo = float(nro_tokens/1000 * valor)

print(f"Com o prompt de {nro_tokens} o custo será de ${custo}")