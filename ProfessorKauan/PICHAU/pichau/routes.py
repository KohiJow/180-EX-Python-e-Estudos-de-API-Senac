from flask import Blueprint, request

from .controllers import (
    listar_eletronicos, buscar_eletronico, criar_eletronico,
    atualizar_eletronico, remover_eletronico,
)

eletronicos_routes = Blueprint('eletronicos_routes', __name__)


def corpo_json():
    # sem Content-Type application/json o Flask levanta 415, com JSON mal formado levanta 400;
    # os dois passam pelo handler de erros e chegam ao cliente como JSON
    return request.get_json()


@eletronicos_routes.get('/Eletronico')
def eletronico_get():
    return listar_eletronicos()


@eletronicos_routes.get('/Eletronico/<int:id>')
def eletronico_get_por_id(id):
    return buscar_eletronico(id)


@eletronicos_routes.post('/Eletronico')
def eletronicos_post():
    return criar_eletronico(corpo_json())


@eletronicos_routes.put('/Eletronico/<int:id>')
def eletronico_put(id):
    return atualizar_eletronico(id, corpo_json())


@eletronicos_routes.delete('/Eletronico/<int:id>')
def eletronico_delete(id):
    return remover_eletronico(id)
