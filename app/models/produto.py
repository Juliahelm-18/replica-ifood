class Produto:
    contador = 0
    produtos_cadastrados = []

    def __init__(self, nome: str, preco: float):
        Produto.contador += 1
        self.pk = Produto.contador
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f'{self.nome}'

    def verifica_nome(self, nome: str) -> bool:
        if len(nome) <= 4:
            return False
        elif nome.isdigit():
            return False
        for produto in Produto.produtos_cadastrados:
            if produto.nome == nome:
                return False
        return True
    
    def verifica_preco(self, preco: float) -> bool:
        if preco <= 0:
            return False
        return True
