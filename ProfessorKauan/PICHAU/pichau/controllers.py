from flask import jsonify, url_for

from .db import db
from .models import Eletronicos
from .validacao import validar_eletronico
from .erros import resposta_erro


def listar_eletronicos():
    eletronicos = db.session.execute(db.select(Eletronicos).order_by(Eletronicos.id)).scalars().all()
    return jsonify({
        'mensagem': 'Lista de eletronicos.',
        'total': len(eletronicos),
        'dados': [eletronico.json() for eletronico in eletronicos]
    })


def buscar_eletronico(id):
    eletronico = db.session.get(Eletronicos, id)
    if eletronico is None:
        return resposta_erro(404, 'Eletronico nao esta no catalogo.')
    return jsonify({'mensagem': 'Eletronico encontrado', 'eletronico': eletronico.json()})


def criar_eletronico(dados):
    limpo, erros = validar_eletronico(dados)
    if erros:
        return resposta_erro(400, 'Dados invalidos.', erros)

    novo_eletronico = Eletronicos(**limpo)
    db.session.add(novo_eletronico)
    db.session.commit()

    resposta = jsonify({'mensagem': 'Eletronico cadastrado com sucesso', 'eletronico': novo_eletronico.json()})
    resposta.status_code = 201
    resposta.headers['Location'] = url_for('eletronicos_routes.eletronico_get_por_id', id=novo_eletronico.id)
    return resposta


def atualizar_eletronico(id, dados):
    eletronico = db.session.get(Eletronicos, id)
    if eletronico is None:
        return resposta_erro(404, 'Eletronico nao esta no catalogo.')

    limpo, erros = validar_eletronico(dados, parcial=True)
    if erros:
        return resposta_erro(400, 'Dados invalidos.', erros)

    for campo, valor in limpo.items():
        setattr(eletronico, campo, valor)
    db.session.commit()
    return jsonify({'mensagem': 'Eletronico atualizado com sucesso', 'eletronico': eletronico.json()})


def remover_eletronico(id):
    eletronico = db.session.get(Eletronicos, id)
    if eletronico is None:
        return resposta_erro(404, 'Eletronico nao esta no catalogo.')

    removido = eletronico.json()
    db.session.delete(eletronico)
    db.session.commit()
    return jsonify({'mensagem': 'Eletronico removido com sucesso', 'eletronico': removido})
