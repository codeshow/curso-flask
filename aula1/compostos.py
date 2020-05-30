
# Listas:
# indices     0         1       2
cores = ["vermelho", "verde", "azul"]

numeros = [1, 2, 3]
mistura = [1, "bruno", 4.5, True, cores, numeros, [1, 2, 3]]

cores.append("amArelo")
cores.insert(1, "branco")
cores.remove("azul")
print(cores)

# Tuplas
#                0           1        2
identidade = ("Bruno", "456789456-9", 15)

print(f"Nome é {identidade[0]}")
print(f"CPF é {identidade[1]}")
print(f"Idade é {identidade[2]}")

# desempacotamento
nome, cpf, idade = identidade
print(nome, cpf, idade)

# Dicionario  (Array Associativo, HashMap, Object)

pessoa = {
    "nome": "Karla",
    "cpf": "698126741-8",
    "idade": 18,
    "cores_preferidas": cores,
    "numeros_preferidos": numeros
}

pessoa["idade"] = 19
pessoa["canal"] = "@KarlaMag"

print(f"Olá, a {pessoa['nome']} tem {pessoa['idade']} anos.")


# Iteração (pegar um elemento de cada vez)

for cor in cores:
    print(cor.upper())

print("Gabriel"[0])
print("Gabriel"[-1])

for letra in "Gabriel":
    if letra == "i":
        continue
    print(letra)

# List Comprehension
print([letra for letra in "Gabriel"])

# list comprehension filtrada
print([letra for letra in "Gabriel" if letra != "i"])


for chave in pessoa:
    print(chave, ":",  pessoa[chave])


for chave, valor in pessoa.items():
    print(chave, ":", valor)
