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
    cep = Column(String(10))
    logradouro = Column(String(300))
    numero = Column(String(50))
    bairro = Column(String(200))
    cidade = Column(String(200))
    estado = Column(String(50))

    data_atualizacao = Column(DateTime, default=datetime.now(), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, 
                 nome:str, 
                 cpf:str, 
                 status:StatusVisitante,
                 observacao:str,
                 cep:str,
                 logradouro:str, 
                 numero:str, 
                 bairro:str, 
                 cidade:str, 
                 estado:str):
        """
        Cria um Visitante

        Arguments:
            nome: nome do visitante.
            cpf: documento de identificação do visitante.
            status: status atual do visitante.
            observacao: observação sobre o visitante.
            cep: cep do visitante.
            logradouro: logradouro do visitante.
            numero: numero do visitante.
            bairro: bairro do visitante.
            cidade: cidade do visitante.
            estado: estado do visitante.
        """
        self.nome = nome
        self.cpf = cpf
        self.status = status
        self.observacao = observacao
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado


