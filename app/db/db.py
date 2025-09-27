from models.produto import Produto
from models.restaurante import Restaurante


class DB:
    BANCO = {}

    def __init__(self, restaurantes):
        self.restaurantes = [{
            "nome: "nome",
            "Comissão": "comissão",
            "Endereço": "Endereço"
        }]
        self.__configurar_tabelas()

    def criar_restaurante(self, restaurante: Restaurante):
        self.restaurantes.append()

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
