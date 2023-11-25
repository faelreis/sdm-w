from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Configuração do SQLite:
DATABASE_URL = "sqlite:///./folha_pagamento.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarando o modelo da tabela de folha de pagamento usando SQLAlchemy:
Base = declarative_base()

class Colaborador(Base):
    __tablename__ = "colaborador"
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, unique=True, index=True)
    nome = Column(String)
    horas_trabalhadas = Column(Integer)
    valor_hora = Column(Float)

# Criação do banco de dados e tabela:
Base.metadata.create_all(bind=engine)

# Inicialização do aplicativo FastAPI:
app = FastAPI()

# Modelo Pydantic para validação de entrada:
class ColaboradorCreate(BaseModel):
    cpf: str
    nome: str
    horas_trabalhadas: int
    valor_hora: float

# Rotas CRUD:
@app.post("/colaboradores/", response_model=ColaboradorCreate)
def criar_colaborador(colaborador: ColaboradorCreate):
    db = SessionLocal()
    db_colaborador = Colaborador(**colaborador.dict())
    db.add(db_colaborador)
    db.commit()
    db.refresh(db_colaborador)
    db.close()
    return colaborador

@app.get("/colaboradores/{colaborador_id}", response_model=ColaboradorCreate)
def ler_colaborador(colaborador_id: int):
    db = SessionLocal()
    colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    db.close()
    if colaborador:
        return colaborador
    raise HTTPException(status_code=404, detail="Colaborador não encontrado")

@app.get("/colaboradores/", response_model=list[ColaboradorCreate])
def listar_colaboradores():
    db = SessionLocal()
    colaboradores = db.query(Colaborador).all()
    db.close()
    return colaboradores

@app.put("/colaboradores/{colaborador_id}", response_model=ColaboradorCreate)
def atualizar_colaborador(colaborador_id: int, colaborador: ColaboradorCreate):
    db = SessionLocal()
    db_colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    if db_colaborador:
        for key, value in colaborador.dict().items():
            setattr(db_colaborador, key, value)
        db.commit()
        db.refresh(db_colaborador)
        db.close()
        return db_colaborador
    raise HTTPException(status_code=404, detail="Colaborador não encontrado")

@app.delete("/colaboradores/{colaborador_id}", response_model=ColaboradorCreate)
def deletar_colaborador(colaborador_id: int):
    db = SessionLocal()
    colaborador = db.query(Colaborador).filter(Colaborador.id == colaborador_id).first()
    if colaborador:
        db.delete(colaborador)
        db.commit()
        db.close()
        return colaborador
    raise HTTPException(status_code=404, detail="Colaborador não encontrado")

# Rotas específicas para a folha de pagamento:
@app.get("/pagamento/total", response_model=float)
def calcular_total_pagamento():
    db = SessionLocal()
    total_pagamento = db.query(Colaborador.horas_trabalhadas * Colaborador.valor_hora).all()
    db.close()
    return sum(total_pagamento)

@app.get("/pagamento/menor", response_model=float)
def calcular_menor_pagamento():
    db = SessionLocal()
    menor_pagamento = db.query(Colaborador.horas_trabalhadas * Colaborador.valor_hora).order_by(Colaborador.horas_trabalhadas * Colaborador.valor_hora).first()
    db.close()
    return menor_pagamento

@app.get("/pagamento/maior", response_model=float)
def calcular_maior_pagamento():
    db = SessionLocal()
    maior_pagamento = db.query(Colaborador.horas_trabalhadas * Colaborador.valor_hora).order_by(Colaborador.horas_trabalhadas * Colaborador.valor_hora.desc()).first()
    db.close()
    return maior_pagamento

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
