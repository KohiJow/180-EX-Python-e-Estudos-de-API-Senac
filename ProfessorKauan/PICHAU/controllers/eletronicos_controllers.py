from models.eletronicos_models import Eletronicos
from db import db
import json
from flask import make_response #qq isso faz?

def get_all_eletronicos():
    eletronicos = Eletronicos.query.all()
    response = make_response(
        json.dumps({
            'mensagem:': 'Lista de eletronicos.',
            'dados': [eletronico.json() for eletronico in eletronicos]
        }, ensure_ascii=False, sort_keys=False)
    )
    response.headers['Content-Type'] = 'application/json'
    return response

def get_all_eletronicos_com_id(id):
    eletronicos = Eletronicos.query.get(id)
    if not eletronicos:
        response = make_response(
            json.dumps({'mensagem: ': 'Eletronico nao esta no catalogo.'}, ensure_ascii=False),
            404
        )

    else:
        response = make_response(
            json.dumps({
                'mensagem': 'Eletronico encontrado',
                'eletronico': eletronicos.json()
            }, ensure_ascii=False, sort_keys=False)
        )
    response.headers['Content-Type'] = 'application/json'
    return response

def create_eletronico(eletronico_data):
    if not all(key in eletronico_data for key in ['nome','categoria', 'preco', 'modelo', 'ano']):
        response = make_response(
            json.dumps({'mensagem': 'Dados invalidos. nome, categoria, preco, modelo e ano sao obrigatorios.'}, ensure_ascii=False),
            400
        )
        response.headers['Content-type'] = 'application/json'
        return response
    
    novo_eletronico= Eletronicos(
    nome = eletronico_data['nome'],
    categoria = eletronico_data['categoria'],
    preco = eletronico_data['preco'],
    modelo = eletronico_data['modelo'],
    ano= eletronico_data['ano']
    )
    
    db.session.add(novo_eletronico) #isso adiciona o eletronico novo no banco de dados?
    db.session.commit() #e isso comita?
    
    response = make_response(
        json.dumps({
            'mensagem': 'Eletronico cadastrado com sucesso',
            'eletronico': novo_eletronico.json()
        }, ensure_ascii= False,sort_keys=False) #praq serve sortkeys? dump json?
    )
    response.headers['content-type'] = 'application/json'
    return response