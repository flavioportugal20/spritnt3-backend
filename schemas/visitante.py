from pydantic import BaseModel
from typing import List
from model import Visitante, StatusVisitante

from datetime import datetime
from util.data_util import DataUtil

class VisitanteSchema(BaseModel):
    """ Define como um novo visitante a ser inserido deve ser representado
    """
    nome: str = "Flávio Portugal"
    cpf: str = "123.456.789-10"
    status: str = "ATIVO"
    observacao: str = "Analista de Sistemas"
    cep: str = "24020085"
    logradouro: str = "Rua da Conceição"
    numero: str = "101"
    bairro: str = "Centro"
    cidade: str = "Niterói"
    estado: str = "RJ"

class VisitanteUpdateSchema(BaseModel):
    """ Define como um novo visitante a ser atualizado deve ser representado
    """
    id: int = 1
    nome: str = "Flávio Portugal"
    cpf: str = "123.456.789-10"
    status: str = "ATIVO"
    observacao: str = "Analista de Sistemas"
    cep: str = "24020085"
    logradouro: str = "Rua da Conceição"
    numero: str = "101"
    bairro: str = "Centro"
    cidade: str = "Niterói"
    estado: str = "RJ"


class VisitanteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do visitante.
    """
    id: int = 1

class RetornoInsertVisitanteSchema(BaseModel):
    """ Define como uma mensagem de retorno de insert será representada
    """
    mesage: str
    id: int

class ListagemVisitantesSchema(BaseModel):
    """ Define como uma listagem de visitantes será retornada.
    """
    visitantes:List[VisitanteSchema]

def apresenta_visitantes(visitantes: List[Visitante]):
    """ Retorna uma representação do visitante seguindo o schema definido em
        VisitanteViewSchema.
    """
    result = []
    for visitante in visitantes:
        result.append({
            "id": visitante.id,
            "nome": visitante.nome,
            "cpf": visitante.cpf,
            "status": visitante.status.value,
            "observacao": visitante.observacao,
            "cep": visitante.cep,
            "logradouro": visitante.logradouro,
            "numero": visitante.numero,
            "bairro": visitante.bairro,
            "cidade": visitante.cidade,
            "estado": visitante.estado,
            "data_atualizacao": DataUtil.formatar(visitante.data_atualizacao),
            "data_criacao": DataUtil.formatar(visitante.data_criacao)
        })

    return {"visitantes": result}

class VisitanteViewSchema(BaseModel):
    """ Define como um visitante será retornado.
    """
    id: int = 1
    nome: str = "Flávio Portugal"
    cpf: str = "123.456.789-10"
    status: StatusVisitante = StatusVisitante.ATIVO
    observacao: str = "Analista de Sistemas"
    cep: str = "24020085"
    logradouro: str = "Rua da Conceição"
    numero: str = "101"
    bairro: str = "Centro"
    cidade: str = "Niterói"
    estado: str = "RJ"
    data_atualizacao: datetime = DataUtil.formatar(datetime.now())
    data_criacao: datetime = DataUtil.formatar(datetime.now())


class VisitanteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    cpf: str

class CountVisitanteViewSchema(BaseModel):
    """ Define como a quantidade de visitantes deve ser retornada.
    """
    count: int = 1

def apresenta_visitante(visitante: Visitante):
    """ Retorna uma representação do visitante seguindo o schema definido em
        VisitanteViewSchema.
    """
    return {
        "id": visitante.id,
        "nome": visitante.nome,
        "cpf": visitante.cpf,
        "status": visitante.status.name,
        "observacao": visitante.observacao,
        "cep": visitante.cep,
        "logradouro": visitante.logradouro,
        "numero": visitante.numero,
        "bairro": visitante.bairro,
        "cidade": visitante.cidade,
        "estado": visitante.estado,
        "data_atualizacao": DataUtil.formatar(visitante.data_atualizacao),
        "data_criacao": DataUtil.formatar(visitante.data_criacao),
    }
