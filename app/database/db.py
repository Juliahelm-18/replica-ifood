# app/database/db.py
import json
import os
from app.models.produto import Produto
from app.models.restaurante import Restaurante

class DB:
    """
    Classe responsável por gerenciar o banco de dados em memória
    e persistir os dados no arquivo 'banco_dados.json'.
    """
    BANCO = {}

    def __init__(self):
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados do arquivo JSON, ou cria estrutura inicial."""
        if os.path.exists('banco_dados.json'):
            with open('banco_dados.json', 'r', encoding='utf-8') as arquivo:
                self.BANCO = json.load(arquivo)
        else:
            self.BANCO = {'RESTAURANTES': []}

    def salvar_dados(self):
        """Salva os dados atuais no arquivo JSON."""
        with open('banco_dados.json', 'w', encoding='utf-8') as arquivo:
            json.dump(self.BANCO, arquivo, indent=4, ensure_ascii=False)

    # ----------------- Restaurantes -----------------

    def criar_restaurante(self, restaurante: Restaurante):
        """Cria um restaurante e salva no banco."""
        if not Restaurante.validar_email(restaurante.email):
            print("Email inválido")
            return None
        if not Restaurante.validar_senha(restaurante.senha):
            print("Senha inválida")
            return None
        if not Restaurante.validar_nome(restaurante.restaurante_nome):
            print("Nome do restaurante inválido")
            return None
        if not Restaurante.validar_comissao(restaurante.comissao):
            print("Comissão inválida")
            return None

        for rest in self.BANCO['RESTAURANTES']:
            if rest['email'] == restaurante.email:
                print("Email já cadastrado!")
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
        print(f"Restaurante {restaurante.restaurante_nome} criado com sucesso")
        return restaurante_dict

    def login(self, email: str, senha: str):
        """Valida login do restaurante."""
        email = email.lower()
        for restaurante in self.BANCO['RESTAURANTES']:
            if restaurante['email'] == email and restaurante['senha'] == senha:
                print(f"Login realizado com sucesso. Bem-vindo, {restaurante['restaurante_nome']}!")
                return restaurante
        print("Email ou senha incorretos.") 
        return None

    def obter_usuario(self, email: str):
        """Retorna um restaurante pelo email."""
        email = email.lower()
        for restaurante in self.BANCO['RESTAURANTES']:
            if restaurante['email'] == email:
                return restaurante
        return None

    def deletar_usuario(self, email: str):
        """Deleta restaurante pelo email."""
        email = email.lower()
        for restaurante in self.BANCO['RESTAURANTES']:
            if restaurante['email'] == email:
                self.BANCO['RESTAURANTES'].remove(restaurante)
                self.salvar_dados()
                print(f"Restaurante {restaurante['restaurante_nome']} deletado com sucesso.")
                return True
        print("Restaurante não encontrado.")
        return False

    def obter_restaurantes(self):
        """Retorna lista de restaurantes ordenada por comissão e nome."""
        restaurantes = self.BANCO['RESTAURANTES'][:]
        for c in restaurantes:
            if 'menu' not in c:
                c['menu'] = []

        com_comissao = [r for r in restaurantes if r.get('comissao') is not None]
        sem_comissao = [r for r in restaurantes if r.get('comissao') is None]

        com_comissao.sort(key=lambda r: (r['comissao'], r['restaurante_nome']))
        sem_comissao.sort(key=lambda r: r['restaurante_nome'])
        return com_comissao + sem_comissao

    def obter_restaurante(self, email: str, senha: str) -> dict | None:
        """Retorna restaurante específico pelo email e senha."""
        email = email.lower()
        for c in self.BANCO['RESTAURANTES']:
            if c['email'] == email and c['senha'] == senha:
                print(f"Login realizado com sucesso. Bem-vindo, {c['restaurante_nome']}!")
                return c  
        print("Email ou senha incorretos.")
        return None

    # ----------------- Produtos -----------------

    def adicionar_produto(self, email: str, senha: str, produto: Produto):
        """Adiciona um produto ao menu de um restaurante autenticado."""
        restaurante = self.login(email, senha)
        if restaurante is None:
            print("Email ou senha incorretos. Não foi possível adicionar o produto.")
            return False

        if 'menu' not in restaurante:
            restaurante['menu'] = []

        for prod in restaurante.get('menu', []):
            if prod['nome'] == produto.nome:
                print(f"Produto {produto.nome} já existe no menu do restaurante.")
                return False

        restaurante['menu'].append(produto.__dict__)
        self.salvar_dados()
        print(f"Produto {produto.nome} adicionado ao restaurante {restaurante['restaurante_nome']}")
        return True


# ----------------- Instância global -----------------
DATABASE = DB()
