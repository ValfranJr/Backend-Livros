# API de livros
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets

app = FastAPI()

MEU_USUARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()

# Dicionário para armazenar os livros cadastrados
meus_livros = {}


class Livro(BaseModel):
    nome: str
    autor: str
    ano: int


def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Basic"},
        )


# Rota para retornar uma mensagem na tela inicial
@app.get("/")
def hello_world():
    return {"Hello": "World"}


# Rota para listar os livros cadastrados
@app.get("/livros")
def get_livros(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit inválidos.")
    if not meus_livros:
        raise HTTPException(status_code=404, detail="Nenhum livro cadastrado.")

    start = (page - 1) * limit
    end = start + limit

    livros_paginados = [
        {
            "id": id_livro,
            "nome": meus_livros[id_livro]["nome"],
            "autor": meus_livros[id_livro]["autor"],
            "ano": meus_livros[id_livro]["ano"],
        }
        for id_livro in meus_livros
        if start <= id_livro < end
    ]

    return [
        {
            "page": page,
            "limit": limit,
            "total": len(meus_livros),
            "livros": livros_paginados,
        }

    ]


# Rota para cadastrar um livro
@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já cadastrado.")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "Livro cadastrado com sucesso."}


# Rota para atualizar um livro
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "Livro atualizado com sucesso."}


# Rota para excluir um livro
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        del meus_livros[id_livro]
        return {"message": "Livro excluído com sucesso."}
