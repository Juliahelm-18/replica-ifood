from fastapi import APIRouter

router = APIRouter(prefix="/restaurants", tags=["Restaurantes"])

# POST /RESTAURANTS 
@router.post('/')
def criar_restaurante():
    return {'message': 'Restaurante criado, amem!'}
# POST /RESTAURANTS/MENU
@router.post('/menu')
def adicionar_item_menu(item: dict):
    return {'message': 'Item adicionado ao menu com sucesso'}

# DELETE /RESTAURANTS/MENU
@router.delete('/menu')
def deletar_item_menu(item_id: int):
    return {'message': f'Item {item_id} deletado do menu com sucesso'}

# GET /RESTAURANTS
@router.get("/")
def listar_restaurantes(email: str = None, senha: str = None):
    return {"message": "Lista de restaurantes fofineos :3"}
# PATCH /RESTAURANTS
@router.patch("/")
def atualizar_restaurante():
    return {'message': 'Restaurante atualizado, gloria!!!!'}