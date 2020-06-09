from loja.modelos import Categoria, Produto

cadeira = Produto("Cadeira", categoria=Categoria("Moveis"))
teclado = Produto("HyperX", categoria=Categoria("Eletronico"))

print(cadeira.nome, cadeira.categoria.nome)
print(teclado.nome, teclado.categoria.nome)
