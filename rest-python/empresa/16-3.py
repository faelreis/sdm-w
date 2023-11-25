from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Configuração do SQLite:
DATABASE_URL = "sqlite:///./estoque.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarando o modelo da tabela de estoque usando SQLAlchemy:
Base = declarative_base()

class Produto(Base):
    __tablename__ = "produto"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, unique=True, index=True)
    nome = Column(String)
    quantidade = Column(Integer)
    preco = Column(Float)

# Criação do banco de dados e tabela:
Base.metadata.create_all(bind=engine)

# Inicialização do aplicativo FastAPI:
app = FastAPI()

# Modelo Pydantic para validação de entrada:
class ProdutoCreate(BaseModel):
    codigo: int
    nome: str
    quantidade: int
    preco: float

class ProdutoUpdate(BaseModel):
    quantidade: int
    preco: float

# Rotas CRUD:
@app.post("/produtos/", response_model=ProdutoCreate)
def criar_produto(produto: ProdutoCreate):
    db = SessionLocal()
    db_produto = Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    db.close()
    return produto

@app.get("/produtos/{produto_id}", response_model=ProdutoCreate)
def ler_produto(produto_id: int):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    db.close()
    if produto:
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.get("/produtos/", response_model=list[ProdutoCreate])
def listar_produtos():
    db = SessionLocal()
    produtos = db.query(Produto).all()
    db.close()
    return produtos

@app.put("/produtos/{produto_id}", response_model=ProdutoCreate)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate):
    db = SessionLocal()
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        for key, value in produto.dict().items():
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
        db.close()
        return db_produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.patch("/produtos/{produto_id}", response_model=ProdutoCreate)
def atualizar_parcial_produto(produto_id: int, produto: ProdutoUpdate):
    db = SessionLocal()
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        for key, value in produto.dict().items():
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
        db.close()
        return db_produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/produtos/{produto_id}", response_model=ProdutoCreate)
def deletar_produto(produto_id: int):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
        db.close()
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Rotas específicas para o estoque:
@app.get("/estoque/total", response_model=int)
def calcular_total_estoque():
    db = SessionLocal()
    total_estoque = db.query(Produto.quantidade).all()
    db.close()
    return sum(total_estoque)

@app.get("/estoque/{produto_id}", response_model=int)
def consultar_quantidade_estoque(produto_id: int):
    db = SessionLocal()
    quantidade_estoque = db.query(Produto.quantidade).filter(Produto.id == produto_id).first()
    db.close()
    if quantidade_estoque:
        return quantidade_estoque[0]
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.get("/estoque/menor", response_model=int)
def consultar_menor_quantidade_estoque():
    db = SessionLocal()
    menor_quantidade_estoque = db.query(Produto.quantidade).order_by(Produto.quantidade).first()
    db.close()
    if menor_quantidade_estoque:
        return menor_quantidade_estoque[0]
    raise HTTPException(status_code=404, detail="Estoque vazio")

@app.get("/estoque/maior", response_model=int)
def consultar_maior_quantidade_estoque():
    db = SessionLocal()
    maior_quantidade_estoque = db.query(Produto.quantidade).order_by(Produto.quantidade.desc()).first()
    db.close()
    if maior_quantidade_estoque:
        return maior_quantidade_estoque[0]
    raise HTTPException(status_code=404, detail="Estoque vazio")

@app.get("/estoque/valor_total", response_model=float)
def calcular_valor_total_estoque():
    db = SessionLocal()
    valor_total_estoque = db.query(Produto.quantidade * Produto.preco).all()
    db.close()
    return sum(valor_total_estoque)

@app.put("/estoque/venda/{produto_id}", response_model=int)
def realizar_venda(produto_id: int, quantidade_vendida: int):
    db = SessionLocal()
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto and db_produto.quantidade >= quantidade_vendida:
        db_produto.quantidade -= quantidade_vendida
        db.commit()
        db.refresh(db_produto)
        db.close()
        return quantidade_vendida
    raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")

@app.put("/estoque/compra/{produto_id}", response_model=int)
def realizar_compra(produto_id: int, quantidade_comprada: int):
    db = SessionLocal()
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        db_produto.quantidade += quantidade_comprada
        db.commit()
        db.refresh(db_produto)
        db.close()
        return quantidade_comprada
    raise HTTPException(status_code=404, detail="Produto não encontrado")
