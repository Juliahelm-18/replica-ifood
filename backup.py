import json
import os
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
class Validador:
    @staticmethod
    def valida_comissao(comissao: int) -> bool:
        if comissao >= 0:
            return True
        return False
    
    @staticmethod
    def valida_email(email: str) -> bool:
        import re
        regex = r'^[a-zA-Z0-9]@[a-zA-Z0-9].[a-z]'
        # muito legal 
        if re.search(regex, email):
            return True
        return False

    @staticmethod
    def valida_senha(senha: str) -> bool:
        if len(senha) < 5:
            return False
        if not any(caracter.isupper() for caracter in senha):
            return False
        if not any(caracter.islower() for caracter in senha):
            return False
        if not any(caracter.isdigit() for caracter in senha):
            return False
        return True
    
    @staticmethod
    def valida_nome_restaurante(restaurante_nome: str) -> bool:
        if len(restaurante_nome) > 10:
            return True
        return False 

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

class DB:
    def __init__(self, arquivo = 'db.json'):
        self.arquivo = arquivo
        self.restaurantes = []
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r') as f:
                dados = json.load(f)
                for r in dados.get('restaurantes', []):
                    restaurante = Restaurante(
                        email=r['email'],
                        senha=r['senha'],
                        restaurante_nome=r['restaurante_nome'],
                        comissao=r['comissao']
                    )
                    self.restaurantes.append(restaurante)
        else:
            with open(self.arquivo, 'w') as f:
                json.dump({"restaurantes": []}, f)

    def salvar(self):
        with open(self.arquivo, 'w') as f:
            json.dump({"restaurantes": [r.dicionario() for r in self.restaurantes]}, f)

    def cadastrar_restaurante(self, email: str, senha: str, nome: str):
        # Verifica duplicidade de email
        if any(r.email == email for r in self.restaurantes):
            raise ValueError("Email já cadastrado.")
        restaurante = Restaurante(email, senha, nome)
        self.restaurantes.append(restaurante)
        self.salvar()
        return restaurante

    def listar_restaurantes(self):
        return [r.restaurante_nome for r in self.restaurantes]

    def encontrar_restaurante(self, email: str, senha: str) -> Restaurante:
        restaurante_encontrado = None
        try:
            for r in self.restaurantes:
                if r.autenticar(email, senha):
                    restaurante_encontrado = r
                    break
            if restaurante_encontrado is None:
                raise ValueError("Email ou senha inválidos.")  
        except ValueError as e:
            print("Erro:", e)
            return None  
        return restaurante_encontrado

    def adicionar_produto(self, email: str, senha: str, nome: str, preco: float):
        restaurante = self.encontrar_restaurante(email, senha)
        if restaurante is None:
            return None
        produto = restaurante.adicionar_produto(email, senha, nome, preco)
        self.salvar()
        return produto

    def remover_produto_api(self, email: str, senha: str, product_id: int):
        restaurante = self.encontrar_restaurante(email, senha)
        produto = restaurante.remover_produto(email, senha, product_id)
        self.salvar()
        return produto

    def listar_restaurantes_com_menu(self):
        def chave_ordem(r: Restaurante):
            comissao_valor = r.comissao if r.comissao and r.comissao > 0 else float('inf')
            # legal
            return (comissao_valor, r.restaurante_nome.lower())
        
        restaurantes_ordenados = sorted(self.restaurantes, key=chave_ordem)

        lista_completa = []
        for r in restaurantes_ordenados:
            menu = [f"{p.nome} - R${p.preco:.2f}" for p in r.menu]
            lista_completa.append({
                "restaurante": r.restaurante_nome,
                "comissao": r.comissao,
                "menu": menu
            })
        return lista_completa

    def atualizar_comissao(self, email: str, senha: str, comissao: int):
        try:
            restaurante = self.encontrar_restaurante(email, senha)
            if not Validador.valida_comissao(comissao):
                print("Comissão inválida. Deve ser maior ou igual a zero.")
                return None
            restaurante.comissao = comissao
            self.salvar()
            print(f"Comissão do restaurante '{restaurante.restaurante_nome}' atualizada para {comissao}%.")
            return restaurante
        except Exception as e:
            print("Erro ao atualizar comissão:", e)
            return None
        
