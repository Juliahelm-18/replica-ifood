# Sistema para gerenciamento de dados de restaurantes e produtos
import json
import os
from app.models.produto import Produto
from app.models.restaurante import Restaurante

class DB:
    BANCO = {}

    def __init__(self):
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists('banco_dados.json'):
            with open('banco_dados.json', 'r', encoding='utf-8') as arquivo:
                self.BANCO = json.load(arquivo)
        else:
            self.BANCO = {'RESTAURANTES': []}
    # Salva os dados atuais no arquivo JSON
    # Se o arquivo não existir, ele será criado

    def salvar_dados(self):
        with open('banco_dados.json', 'w', encoding='utf-8') as arquivo:
            json.dump(self.BANCO, arquivo, indent=4, ensure_ascii=False)
    

    def criar_restaurante(self, restaurante: Restaurante):
        if not Restaurante.validar_email(restaurante.email):
            return None
        if not Restaurante.validar_senha(restaurante.senha):
            return None
        if not Restaurante.validar_nome(restaurante.restaurante_nome):
            return None
        if not Restaurante.validar_comissao(restaurante.comissao):
            return None

        for rest in self.BANCO['RESTAURANTES']:
            if rest['email'] == restaurante.email:
                return None

        restaurante_dict = {
            "pk": restaurante.pk,
            "email": restaurante.email,
            "senha": restaurante.senha,
            "restaurante_nome": restaurante.restaurante_nome,
            "comissao": restaurante.comissao,
            "menu": []
        }

        self.BANCO['RESTAURANTES'].append(restaurante_dict)
        self.salvar_dados()
        return restaurante_dict

    def login(self, email: str, senha: str):
        email = email.lower()
        for restaurante in self.BANCO['RESTAURANTES']:
            if restaurante['email'] == email and restaurante['senha'] == senha:
                return restaurante
        return None

    def obter_usuario(self, email: str):
        email = email.lower()
        for restaurante in self.BANCO['RESTAURANTES']:
            if restaurante['email'] == email:
                return restaurante
        return None

    def deletar_usuario(self, email: str):
        email = email.lower()
        for restaurante in self.BANCO['RESTAURANTES']:
            if restaurante['email'] == email:
                self.BANCO['RESTAURANTES'].remove(restaurante)
                self.salvar_dados()
                return True
        return False
    
    def obter_restaurantes(self):
        restaurantes = self.BANCO['RESTAURANTES'][:]
        for rest in restaurantes:
            if 'menu' not in rest:
                rest['menu'] = []

        # Separa com e sem comissão
        com_comissao = [r for r in restaurantes if r['comissao'] is not None]
        sem_comissao = [r for r in restaurantes if r['comissao'] is None]

        # Ordena com comissão: maior para menor
        def ordenar_comissao_desempate(r):
            return (-r['comissao'], r['restaurante_nome'].lower())
        com_comissao.sort(key=ordenar_comissao_desempate)

        # Desempata pelo nome
        sem_comissao.sort(key=lambda r: r['restaurante_nome'].lower())
        # Retorna somente os campos necessários
        resultado = [
            {
                "restaurante_nome": r["restaurante_nome"],
                "comissao": r["comissao"],
                "menu": r.get("menu", [])
            }
            for r in (com_comissao + sem_comissao)
        ]
        return resultado

    def obter_restaurante(self, email: str, senha: str) -> dict | None:
        email = email.lower()
        for rest in self.BANCO['RESTAURANTES']:
            if rest['email'] == email and rest['senha'] == senha:
                return rest
        return None

    def adicionar_produto(self, email: str, senha: str, produto: Produto):
        restaurante = self.login(email, senha)
        if restaurante is None:
            return False

        if 'menu' not in restaurante:
            restaurante['menu'] = []

        for prod in restaurante.get('menu', []):
            if prod['nome'] == produto.nome:
                return False

        restaurante['menu'].append(produto.__dict__)
        self.salvar_dados()
        return True

DATABASE = DB()
