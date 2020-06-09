class Animal:
    # atributos de classe
    planeta = "Terra"
    _animal_nasceu = False

    # encapsulamento com propriedades
    @property
    def nasceu(self):
        return self._animal_nasceu

    # métodos der instância
    def nascer(self):
        self._animal_nasceu = True
        print(f"Oi eu nasci no {self.planeta}")

    def comer(self):
        print("Estou comendo.. crunch crunch")


class Mamifero(Animal):
    # herança

    def comer(self):
        print("Estou tomando leite...")


class Oviparos(Animal):

    def nascer(self):
        print(f"Acabei de quebrar o ovo no planeta {self.planeta}")


class Especial(Mamifero, Oviparos):
    # herança multipla/mixins

    def nadar(self):
        print("Tchiubummmm")
