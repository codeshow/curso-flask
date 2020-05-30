
counter = 0

while counter < 25:
    print(f"Hello {counter}")
    counter += 1
    if counter == 12:
        break

continuar = "sim"
while continuar == "sim":
    print(input("Qual seu nome?"))
    continuar = input("continuar?")
