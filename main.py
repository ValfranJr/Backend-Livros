# API de livros
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
# Dicionário para armazenar os livros cadastrados
meus_livros = {}


class Livro(BaseModel):
    nome: str
    autor: str
    ano: int

# Rota para retornar uma mensagem na tela inicial
@app.get("/")
def hello_world():
    return {"Hello": "World"}

# Rota para listar os livros cadastrados
@app.get("/livros")
def get_livros():
    if not meus_livros:
        return {"message": "Não há livros cadastrados."}
    else:
        return {"livros": meus_livros}


# Rota para cadastrar um livro
@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já cadastrado.")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "Livro cadastrado com sucesso."}


# Rota para atualizar um livro
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        meus_livros[id_livro] = livro.model_dump()
        return {"message": "Livro atualizado com sucesso."}


# Rota para excluir um livro
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        del meus_livros[id_livro]
        return {"message": "Livro excluído com sucesso."}
