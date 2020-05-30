a = 0
b = 10


# EAFP

try:
    b.upper()
    print(b // a)
except AttributeError as e:
    print("Nao posso tranformar n em maiusculo", str(e))
except ZeroDivisionError as e:
    print("Deu Erro tenta de novo", str(e))
