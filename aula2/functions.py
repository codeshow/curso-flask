
valor = "Eu sou global"


def ola(nome, cpf, idade=0, maiusculo=False, *args, **kwargs):
    """Essa função diz OLá.

    :param nome str: Nome da pessoa
    :param cpf str: Nome da pessoa
    :param idade int: Nome da pessoa

    :param args: Argumentos extras posicionais
    :param kwargs: Argumentos extras nomeados

    :returns None:
    """

    valor = "Eu sou local"

    def funcao_dentro_de_funcao():  # inner function / closure
        nonlocal valor
        valor = "Mudando a variavel do escopo imediatamente anterior!"

    def outra_closure():
        global valor
        valor = "Mudando a variavel global"

    print(args)
    print(kwargs)

    if maiusculo:
        msg = f"Olá, {nome}".upper()
    else:
        msg = f"Olá, {nome}, {cpf}, idade: {idade}"

    print(msg)


ola("Grad", "123123")
ola("Karla", cpf="123123", maiusculo=True)
ola("Lysandro", "123123", False)


# Desempacotamento de listas/tuplas
pessoa = ['Karla', '4589456-45', 15]
ola(*pessoa)


# Desempacotamento de Dicionários
pessoa = {
    'nome': 'Karla',
    'cpf': '4589456-45',
    'idade': 15
}
ola(**pessoa)

# Chamada com argumentos extra
ola("Karla", "123123", idade=21, maiusculo=True, foo="bar", outra_coisa=1)
