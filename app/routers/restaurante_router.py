from fastapi import APIRouter
from app.database.db import DATABASE
from app.models.produto import Produto
from app.models.restaurante import Restaurante

router = APIRouter(prefix="/restaurants", tags=["Restaurantes"])
database = DATABASE

# POST /restaurants
@router.post('/')
def criar_restaurante(email: str, senha: str, restaurante_nome: str, comissao: float = None):
    # Função responsável por criar um novo restaurante no sistema.
    # Recebe os dados do restaurante, instancia um objeto Restaurante e o envia para o banco de dados.
    novo_restaurante = Restaurante(
        email=email,
        senha=senha,
        restaurante_nome=restaurante_nome,
        comissao=comissao
    )
    resultado = database.criar_restaurante(novo_restaurante)
    if resultado:
        return {"message": f"Restaurante {novo_restaurante.restaurante_nome} criado com sucesso!"}
    return {"message": "Falha ao criar restaurante."}

# POST /restaurants/menu
@router.post('/menu')
def adicionar_item_menu(email: str, senha: str, nome: str, preco: float):
    # Função responsável por adicionar um novo produto ao menu de um restaurante.
    # Valida o nome e o preço do produto antes de cadastrá-lo.
    produto = Produto(nome=nome, preco=preco)

    if not produto.verifica_nome():
        return {"message": "Falha: nome do produto inválido (mínimo 5 caracteres, não numérico ou já cadastrado)."}
    
    if not Produto.verifica_preco(produto.preco):
        return {"message": "Falha: preço do produto inválido (deve ser > 0)."}

    sucesso = database.adicionar_produto(email, senha, produto)
    if sucesso:
        return {"message": f"Produto {produto.nome} adicionado ao menu com sucesso! Sua pk é {produto.pk}."}

    return {"message": "Falha ao adicionar produto, verifique email/senha ou produto duplicado no menu."}

# DELETE /restaurants/menu
@router.delete('/menu')
def deletar_item_menu(email: str, senha: str, product_id: int):
    # Função responsável por remover um produto do menu de um restaurante.
    # Verifica as credenciais do restaurante (email e senha) e busca o item pelo ID.
    restaurante = database.obter_restaurante(email, senha)
    if not restaurante or 'menu' not in restaurante:
        return {"message": "Falha ao deletar item, verifique email/senha"}

    for i, item in enumerate(restaurante['menu']):
        if item['pk'] == product_id:
            restaurante['menu'].pop(i)
            database.salvar_dados()
            return {"message": f"Item {item['nome']} deletado do menu com sucesso!"}

    return {"message": "Produto não encontrado no menu do restaurante."}

# GET /restaurants
@router.get("/")
def listar_restaurantes():
    # Retorna lista de restaurantes ordenada por comissão e nome.
    return {"restaurantes": database.obter_restaurantes()}

# PATCH /restaurants
@router.patch("/")
def atualizar_comissao(email: str, senha: str, commission: int):
    # Atualiza a comissão de um restaurante autenticado.
    restaurante = database.obter_restaurante(email, senha)
    if not restaurante:
        return {"message": "Falha ao atualizar restaurante, verifique email/senha"}

    if not Restaurante.validar_comissao(commission):
        return {"message": "Comissão inválida"}

    restaurante['comissao'] = commission
    database.salvar_dados()
    return {"message": f"Comissão do restaurante {restaurante['restaurante_nome']} atualizada com sucesso!"}
