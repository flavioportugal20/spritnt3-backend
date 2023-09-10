from pydantic import BaseModel
from typing import List

from model import TipoAcesso, Acesso
from schemas.visitante import VisitanteViewSchema
from util.data_util import DataUtil


class AcessoSchema(BaseModel):
    """ Define como um novo acesso a ser inserido deve ser representado
    """
    local: str = "331"
    tipo: TipoAcesso = TipoAcesso.VISITA
    observacao: str = "Manutenção do sistema"
    visitante_id: int = 1


class AcessoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do acesso.
    """
    id: int = 1

class RetornoInsertAcessoSchema(BaseModel):
    """ Define como uma mensagem de retorno de insert será representada
    """
    mesage: str
    id: int

class ListagemAcessosSchema(BaseModel):
    """ Define como uma listagem de acessos será retornada.
    """
    acessos:List[AcessoSchema]


def apresenta_acessos(acessos: List[Acesso]):
    """ Retorna uma representação do acesso seguindo o schema definido em
        AcessoViewSchema.
    """
    result = []
    for acesso in acessos:
        result.append({
            "id": acesso.id,
            "local": acesso.local,
            "tipo": acesso.tipo.value,
            "observacao": acesso.observacao,
            "data_acesso": DataUtil.formatar(acesso.data_acesso),
            "visitante": {
                "id": acesso.visitante_obj.id,
                "nome": acesso.visitante_obj.nome,
                "cpf": acesso.visitante_obj.cpf,
                "status": acesso.visitante_obj.status.name,
                "observacao": acesso.visitante_obj.observacao,
                "data_atualizacao": DataUtil.formatar(acesso.visitante_obj.data_atualizacao),
                "data_criacao": DataUtil.formatar(acesso.visitante_obj.data_criacao),
            }
        })

    return {"acessos": result}


class AcessoViewSchema(BaseModel):
    """ Define como um acesso será retornado.
    """
    id: int = 1
    local: str = "331"
    tipo = TipoAcesso.VISITA
    observacao: str = "Manutenção do sistema"
    data_acesso: str = "10/02/2021 12:08:02"
    visitante: VisitanteViewSchema

class AcessoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int
    local: str

class CountAcessoViewSchema(BaseModel):
    """ Define como a quantidade de acessos deve ser retornada.
    """
    count: int = 1

def apresenta_acesso(acesso: Acesso):
    """ Retorna uma representação do acesso seguindo o schema definido em
        AcessoViewSchema.
    """
    return {
        "id": acesso.id,
        "local": acesso.local,
        "tipo": acesso.tipo.value,
        "observacao": acesso.observacao,
        "data_acesso": DataUtil.formatar(acesso.data_acesso),
        "visitante": {
            "id": acesso.visitante_obj.id,
            "nome": acesso.visitante_obj.nome,
            "cpf": acesso.visitante_obj.cpf,
            "status": acesso.visitante_obj.status.name,
            "observacao": acesso.visitante_obj.observacao,
            "data_atualizacao": DataUtil.formatar(acesso.visitante_obj.data_atualizacao),
            "data_criacao": DataUtil.formatar(acesso.visitante_obj.data_criacao),
        }
    }
 