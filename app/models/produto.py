class Produto:
    produto_nome = []
    def __init__(self, email: str, senha: str, nome: str, preco: float):
        self.email = email
        self.senha = senha
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f'{self.nome}'
    
    @staticmethod
    def valida_produto(nome: str, preco: float, produto_nome: list) -> bool:
        if len(nome) < 4:
            return False
        elif preco <= 0:
            return False
        for item in produto_nome:
            if item == nome:
                return False
        produto_nome.append(nome)
        return True
