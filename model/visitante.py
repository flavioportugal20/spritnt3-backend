from sqlalchemy import Column, String, Integer, DateTime, Enum
from datetime import datetime

from  model import Base, StatusVisitante

class Visitante(Base):
    __tablename__ = 'visitante'

    id = Column("pk_visitante", Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    status = Column(Enum(StatusVisitante))
    observacao = Column(String(1000))

    data_atualizacao = Column(DateTime, default=datetime.now(), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, 
                 nome:str, 
                 cpf:str, 
                 status:StatusVisitante,
                 observacao:str):
        """
        Cria um Visitante

        Arguments:
            nome: nome do visitante.
            cpf: documento de identificação do visitante.
            status: status atual do visitante.
            observacao: observação sobre o visitante.
        """
        self.nome = nome
        self.cpf = cpf
        self.status = status
        self.observacao = observacao


