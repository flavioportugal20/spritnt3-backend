from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship, Mapped

from  model import Base, TipoAcesso
from model.visitante import Visitante

class Acesso(Base):
    __tablename__ = 'acesso'

    id = Column(Integer, primary_key=True)
    local = Column(String(250))
    tipo = Column(Enum(TipoAcesso))
    data_acesso = Column(DateTime, default=datetime.now(), nullable=False)
    observacao: str = Column(String(1000))

    # Definição do relacionamento entre o acesso e um visitante.
    # Aqui está sendo definido a coluna 'visitante_id' que vai guardar
    # a referencia ao visitante, a chave estrangeira que relaciona
    # um visitante ao acesso.
    visitante_id = Column(Integer, ForeignKey("visitante.pk_visitante"), nullable=False)
    visitante_obj = relationship("Visitante")

    def __init__(self, local:str, tipo:TipoAcesso, observacao:str, visitante_id:int):              
        """
        Cria um Acesso

        Arguments:
            local: local do acesso do visitante.
            tipo: tipo do acesso.
        """
        self.local = local
        self.tipo= tipo
        self.observacao = observacao
        self.visitante_id = visitante_id

