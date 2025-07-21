# API de livros
from fastapi import FastAPI, HTTPException

app = FastAPI()
# Dicionário para armazenar os livros cadastrados
meus_livros = {}

# Rota para listar os livros cadastrados
@app.get("/livros")
def get_livros():
    if not meus_livros:
        return {"message": "Não há livros cadastrados."}
    else:
        return {"livros": meus_livros}

# Rota para cadastrar um livro
@app.post("/adiciona")
def post_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    if id_livro in meus_livros:
        raise HTTPException(status_code=400, detail="Livro já cadastrado.")
    else:
        meus_livros[id_livro] = {
            "nome": nome_livro,
            "autor": autor_livro,
            "ano": ano_livro
        }
        return {"message": "Livro cadastrado com sucesso."}
# Rota para atualizar um livro
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, nome_livro: str, autor_livro: str, ano_livro: int):
    meu_livro = meus_livros.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        if nome_livro:
            meu_livro["nome"] = nome_livro
        if autor_livro:
            meu_livro["autor"] = autor_livro
        if ano_livro:
            meu_livro["ano"] = ano_livro
        return {"message": "Livro atualizado com sucesso."}

# Rota para excluir um livro
@app.delete("/deletar/{id_livro}")
def delete_livro(id_livro: int):
    if id_livro not in meus_livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    else:
        del meus_livros[id_livro]
        return {"message": "Livro excluído com sucesso."}

