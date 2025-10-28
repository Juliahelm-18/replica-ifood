# Replica iFood

FastAPI + JSON para gerenciamento de restaurantes e menus.

---

## Funcionalidades

- Cadastro/login de restaurantes  
- Adição, listagem e remoção de produtos do menu  
- Listagem de restaurantes ordenada por comissão e nome  
- Persistência em `banco_dados.json`  

---

## Tecnologias

Python 3.13 | FastAPI | Uvicorn | JSON (para armazenamento de dados)  

---

## Como rodar

1 - Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd replica-ifood
```

2 - Instale as dependências
```bash
pip install -r requirements.txt
```

3 - Rode a aplicação
```bash
uvicorn app.main:app --reload
```

4 - Acesse a documentação interativa
```bash
http://127.0.0.1:8000/docs
```

## Endpoints principais
- POST /restaurantes → criar restaurante
- GET /restaurantes → listar restaurantes
- POST /menu → adicionar produto ao menu
- DELETE /menu/{product_id} → remover produto do menu

