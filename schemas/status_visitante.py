from pydantic import BaseModel
from typing import List
from model import StatusVisitante


class StatusVisitanteSchema(BaseModel):
    """ Define como um status visitante deve ser representado
    """
    name: str = "ATIVO"
    value: str = "Ativo"

class ListagemStatusVisitanteSchema(BaseModel):
    """ Define como uma listagem de status visitante será retornada.
    """
    lista_status_visitante:List[StatusVisitanteSchema]

def apresenta_lista_status_visitante():
    """ Retorna uma representação de listagem do status visitante seguindo o schema definido em
        ListagemStatusVisitanteSchema.
    """
    result = []
    for item in StatusVisitante:
        result.append({
            "name": item.name,
            "value": item.value
        })

    return {"lista_status_visitante": result}

