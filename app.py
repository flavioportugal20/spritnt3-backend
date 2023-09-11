from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Visitante, Acesso
from logger import logger
from model.status_visitante import StatusVisitante
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
visitante_tag = Tag(name="Visitante", description="Adição, visualização e remoção de visitantes à base")
acesso_tag = Tag(name="Acesso", description="Adição e visualização de um acesso à um visitante cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/visitante', tags=[visitante_tag],
          responses={"200": RetornoInsertVisitanteSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_visitante(form: VisitanteSchema):
    """Adiciona um novo visitante à base de dados

    Retorna a mensagem de sucesso e o id do visitante.
    """
    visitante = Visitante(
        nome=form.nome,
        cpf=form.cpf,
        status=StatusVisitante[form.status],
        observacao=form.observacao,
        cep=form.cep,
        logradouro=form.logradouro,
        numero=form.numero,
        bairro=form.bairro,
        cidade=form.cidade,
        estado=form.estado)
    logger.debug(f"Adicionando visitante de nome: '{form.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando visitante
        session.add(visitante)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado visitante de nome: '{visitante.nome}'")
        return {"mesage": "Visitante adicionado com sucesso!", "id": visitante.id}, 200

    except IntegrityError as e:
        # como a duplicidade do cpf é a provável razão do IntegrityError
        error_msg = "Visitante de mesmo CPF já salvo na base :/"
        logger.warning(f"Erro ao adicionar visitante '{form.nome}', {e}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/" 
        logger.warning(f"Erro ao adicionar visitante '{form.nome}', {e}")
        return {"mesage": error_msg}, 400


@app.put('/visitante', tags=[visitante_tag],
          responses={"200": VisitanteViewSchema, "409": ErrorSchema, "404": ErrorSchema})
def update_visitante(form: VisitanteUpdateSchema):
    """Atualiza um visitante à base de dados

    Retorna uma representação dos visitantes e acessos associados.
    """
    
    session = Session()
    # fazendo a busca
    visitante = session.query(Visitante).filter(Visitante.id == form.id).first()

    visitante.nome = form.nome
    visitante.cpf = form.cpf
    visitante.status = form.status
    visitante.observacao = form.observacao
    visitante.cep = form.cep
    visitante.logradouro = form.logradouro
    visitante.numero = form.numero
    visitante.bairro = form.bairro
    visitante.cidade = form.cidade
    visitante.estado = form.estado
        
    if not visitante:
        # se o visitante não foi encontrado
        error_msg = "Visitante não encontrado na base :/"
        logger.warning(f"Erro ao buscar visitante '{form.id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Visitante econtrado: '{visitante.nome}'")
        # retorna a representação de visitante
        session.merge(visitante)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado visitante de nome: '{visitante.nome}'")
        return apresenta_visitante(visitante), 200


@app.get('/visitante/lista', tags=[visitante_tag],
         responses={"200": ListagemVisitantesSchema, "404": ErrorSchema})
def get_visitantes():
    """Faz a busca por todos os visitantes cadastrados

    Retorna uma representação da listagem de visitantes.
    """
    logger.debug(f"Coletando visitantes ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    visitantes = session.query(Visitante).order_by(Visitante.id.desc()).all()
    
    if not visitantes:
        # se não há visitantes cadastrados
        return {"visitantes": []}, 200
    else:
        logger.debug(f"%d visitantes encontrados" % len(visitantes))
        # retorna a representação de visitante
        print(visitantes)
        return apresenta_visitantes(visitantes), 200


@app.get('/visitante/lista-status', tags=[visitante_tag],
         responses={"200": ListagemStatusVisitanteSchema, "404": ErrorSchema})
def get_lista_status_visitante():
    """Retorna as opções de status do visitante

    Retorna uma representação da listagem de status de visitante.
    """
    logger.debug(f"Coletando visitantes ")

    # fazendo a busca
    lista_status_visitante = apresenta_lista_status_visitante()

    if not lista_status_visitante:
        # se não há lista status visitante cadastrado
        return {"lista_status_visitante": []}, 200
    else:
        logger.debug(f"%d status visitante encontrados" % len(lista_status_visitante))
        # retorna a representação da listagem do status visitante
        print(lista_status_visitante)
        return lista_status_visitante, 200


@app.get('/visitante', tags=[visitante_tag],
         responses={"200": VisitanteViewSchema, "404": ErrorSchema})
def get_visitante(query: VisitanteBuscaSchema):
    """Faz a busca por um visitante a partir do id

    Retorna uma representação do visitante.
    """
    visitante_id = query.id
    logger.debug(f"Coletando dados sobre visitante #{visitante_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    visitante = session.query(Visitante).filter(Visitante.id == visitante_id).first()

    if not visitante:
        # se o visitante não foi encontrado
        error_msg = "Visitante não encontrado na base :/"
        logger.warning(f"Erro ao buscar visitante '{visitante_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Visitante econtrado: '{visitante.nome}'")
        # retorna a representação de visitante
        return apresenta_visitante(visitante), 200


@app.delete('/visitante', tags=[visitante_tag],
            responses={"200": VisitanteDelSchema, "404": ErrorSchema})
def del_visitante(query: VisitanteBuscaSchema):
    """Deleta um visitante a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    #visitante_id = unquote(unquote(query.id))
    visitante_id = query.id
    print(visitante_id)
    logger.debug(f"Deletando dados sobre visitante #{visitante_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Visitante).filter(Visitante.id == visitante_id).delete()
    session.query(Acesso).filter(Acesso.visitante_id == visitante_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado visitante #{visitante_id}")
        return {"mesage": "Visitante removido", "id": visitante_id}
    else:
        # se o visitante não foi encontrado
        error_msg = "Visitante não encontrado na base :/"
        logger.warning(f"Erro ao deletar visitante #'{visitante_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/visitante/lista/count/bloqueados', tags=[visitante_tag],
            responses={"200": CountVisitanteViewSchema, "404": ErrorSchema})
def count_visitante_bloqueados():
    """Retorna a quantidade de visitantes cadastrados
    """

    # criando conexão com a base
    session = Session()
    count = session.query(Visitante).filter(Visitante.status == 'BLOQUEADO').count()
    session.commit()

    if count and count >= 0:
        # retorna a quantidade de visitantes bloqueados
        logger.debug(f"Quantidade de visitantes bloqueados #{count}")
        return {"count": count}
    else:
        logger.debug(f"Erro ao retornar a quantidade de visitantes bloqueados")
        return {"message": "Erro ao retornar a quantidade de visitantes bloqueados", "count": count}


@app.post('/acesso', tags=[acesso_tag],
          responses={"200": RetornoInsertAcessoSchema, "404": ErrorSchema})
def add_acesso(form: AcessoSchema):
    """Adiciona um novo acesso à um visitante cadastrado na base de dados

    Retorna a mensagem de sucesso e o id do acesso.
    """
    visitante_id  = form.visitante_id

    logger.debug(f"Adicionado acesso ao visitante #{visitante_id}")

    try:
        # criando conexão com a base
        session = Session()
        
        # criando o acesso
        acesso = Acesso(form.local, form.tipo, form.observacao, form.visitante_id)

        # adicionando o acesso
        session.add(acesso)
        session.commit()
        logger.debug(f"Adicionado acesso ao visitante #{visitante_id}")
        return {"mesage": "Acesso adicionado com sucesso!", "id": acesso.id}, 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/" 
        logger.warning(f"Erro ao adicionar acesso ao visitante '{visitante_id}', {e}")
        return {"mesage": error_msg}, 400
    

@app.get('/acesso/lista', tags=[acesso_tag],
         responses={"200": ListagemAcessosSchema, "404": ErrorSchema})
def get_acessos():
    """Faz a busca por todos os acessos cadastrados

    Retorna uma representação da listagem de acessos.
    """
    logger.debug(f"Coletando acessos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    acessos = session.query(Acesso).order_by(Acesso.id.desc()).all()

    if not acessos:
        # se não há acessos cadastrados
        return {"acessos": []}, 200
    else:
        logger.debug(f"%d acessos encontrados" % len(acessos))
        # retorna a representação de acesso
        print(acessos)
        return apresenta_acessos(acessos), 200


@app.get('/acesso', tags=[acesso_tag],
         responses={"200": AcessoViewSchema, "404": ErrorSchema})
def get_acesso(query: AcessoBuscaSchema):
    """Faz a busca por um acesso a partir do id

    Retorna uma representação do acesso.
    """
    acesso_id = query.id
    logger.debug(f"Coletando dados sobre acesso #{acesso_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    acesso = session.query(Acesso).filter(Acesso.id == acesso_id).first()

    if not acesso:
        # se o acesso não foi encontrado
        error_msg = "Acesso não encontrado na base :/"
        logger.warning(f"Erro ao buscar acesso '{acesso_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Acesso econtrado: '{acesso.id}'")
        # retorna a representação de acesso
        return apresenta_acesso(acesso), 200
    

@app.get('/acesso/lista/count', tags=[acesso_tag],
            responses={"200": CountAcessoViewSchema, "404": ErrorSchema})
def count_acesso():
    """Retorna a quantidade de acessos cadastrados
    """

    # criando conexão com a base
    session = Session()
    count = session.query(Acesso).count()
    session.commit()

    if count and count >= 0:
        # retorna a quantidade de acessos cadastrados
        logger.debug(f"Quantidade de acessos #{count}")
        return {"count": count}
    else:
        logger.debug(f"Erro ao retornar a quantidade de acessos cadastrados")
        return {"message": "Erro ao retornar a quantidade de acessos cadastrados", "count": count}


@app.get('/acesso/lista/count/obs', tags=[acesso_tag],
            responses={"200": CountAcessoViewSchema, "404": ErrorSchema})
def count_acesso_obs():
    """Retorna a quantidade de acessos com observações
    """

    # criando conexão com a base
    session = Session()
    count = session.query(Acesso).filter(Acesso.observacao.isnot(None), Acesso.observacao != '').count()
    session.commit()

    if count and count >= 0:
        # retorna a quantidade de acessos cadastrados
        logger.debug(f"Quantidade de acessos com observações #{count}")
        return {"count": count}
    else:
        logger.debug(f"Erro ao retornar a quantidade de acessos com observações")
        return {"message": "Erro ao retornar a quantidade de acessos com observações", "count": count}
    


