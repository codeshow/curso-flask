
def header(function):
    def decorator(*args, **kwargs):
        print("### Bem vindo ao meu site ###\n")
        return function(*args, **kwargs)
    return decorator


def footer(function):
    def decorator(*args, **kwargs):
        print("### Copyright - 2020 ###\n")
        return function(*args, **kwargs)
    return decorator


@footer
@header
def produto(nome):
    print(f"Produto: {nome} - R$ 2k")


@footer
@header
def sobre():
    print("Esta é a minha loja.... conta:")


# produto("Cadeira Gamer")
# produto("Teclado Mecanico")


def pao(f):
    def wrapper():
        print("(fatia superior pao)")
        f()
        print("(fatia inferior pao)")
    return wrapper


@pao
def x_vegan():
    print("hamburguer vegano")


@pao
def opa():
    print("    ")


x_vegan()
opa()
