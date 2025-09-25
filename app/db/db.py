from models.produto import Produto
from models.restaurante import Restaurante


class DB:
    BANCO = {}

    def __init__(self, adicionar_dados_fake=False):
        self.__configurar_tabelas()

    def __configurar_tabelas(self):
        self.BANCO['RESTAURANTES'] = [
            Restaurante(
                pk=1, email='rest1@rest.com', senha='senha', nome_restaurante='Meu Restaurante', comissao=10,
                menu=[
                    Produto(pk=1, nome='Pizza Queijo', preco=10),
                    Produto(pk=2, nome='Pizza Calabresa', preco=12),
                ]
            ),
            Restaurante(
                pk=2, email='rest2@rest.com', senha='senha', nome_restaurante='Melhor Restaurante', comissao=7,
                menu=[]
            )
        ]

    def criar_restaurante(self, restaurante: Restaurante):
        pass

    def login(self, email: str, senha: str):
        pass

    def obter_usuario(self, email: str):
        pass

    def deletar_usuario(self, email: str):
        pass

    def obter_restaurantes(self):
        return self.BANCO['RESTAURANTES']

    def obter_restaurante(self, email: str, senha: str) -> Restaurante | None:
        return self.BANCO['RESTAURANTES'][0]
