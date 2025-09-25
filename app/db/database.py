import json
import os
from app.models.restaurante import Restaurante
from app.utils.validador import Validador

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
