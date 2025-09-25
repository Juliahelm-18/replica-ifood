from models.produto import Produto
from models.restaurante import Restaurante


class DB:
    BANCO = {}

    def __init__(self, adicionar_dados_fake=False):
        self.__configurar_tabelas()



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
