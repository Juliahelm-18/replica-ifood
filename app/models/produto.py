class Produto:
    contador = 0
    produtos_cadastrados = []

    def __init__(self, nome: str, preco: float = None):
        Produto.contador += 1
        self.pk = Produto.contador
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f'{self.nome}'
    
    def verifica_nome(self) -> bool:
        # Verifica se o nome do produto é válido.
        if len(self.nome) <= 4:
            return False
        elif self.nome.isdigit():
            return False
        for produto in Produto.produtos_cadastrados:
            if produto.nome == self.nome:
                return False
        return True

    @staticmethod
    def verifica_preco(preco: float) -> bool:
        # Verifica se o preço do produto é válido.
        if preco <= 0:
            return False
        return True
