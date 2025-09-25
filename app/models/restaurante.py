class Restaurante:
    def __init__(self, email: str, senha: str, restaurante_nome: str, comissao: int):
        self.email = email
        self.senha = senha
        ## usar hash de senha(bcrypt)
        self.restaurante_nome = restaurante_nome
        self.comissao = comissao

    def __str__(self):
        return f'{self.restaurante_nome}'
    
    def dicionario(self):
        return {
            "email": self.email,
            "senha": self.senha,
            "restaurante_nome": self.restaurante_nome,
            "comissao": self.comissao
        }
