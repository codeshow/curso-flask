numero = 4
fracao = 6.1
online = False
texto = "Armando"


if numero == 5:
    print("Hello 5")
elif numero == 4 or online:
    print("Hello 4")
else:
    print("Final")


print("Ola estou online" if online else "Ola estou offline")
