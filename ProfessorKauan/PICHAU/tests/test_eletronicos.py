import json

import pytest

from pichau import create_app
from pichau.dados import CATALOGO_INICIAL, carregar_catalogo_inicial
from pichau.validacao import ANO_MINIMO, ano_maximo

VALIDO = {'nome': 'Monitor', 'categoria': 'Periférico', 'preco': 899.9, 'modelo': '27 polegadas', 'ano': 2024}

CONFIG_TESTE = {
    'TESTING': True,
    # banco em memoria: cada teste comeca do zero e nada e gravado em disco
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
}


@pytest.fixture
def app():
    return create_app(CONFIG_TESTE)


@pytest.fixture
def client(app):
    return app.test_client()


def post(client, corpo):
    return client.post('/Eletronico', json=corpo)


# ---- GET /Eletronico

def test_listar_devolve_catalogo_inicial(client):
    resposta = client.get('/Eletronico')
    assert resposta.status_code == 200
    assert resposta.mimetype == 'application/json'
    corpo = resposta.get_json()
    assert corpo['mensagem'] == 'Lista de eletronicos.'
    assert corpo['total'] == len(CATALOGO_INICIAL)
    assert [item['nome'] for item in corpo['dados']] == [item['nome'] for item in CATALOGO_INICIAL]
    assert list(corpo['dados'][0]) == ['id', 'nome', 'categoria', 'preco', 'modelo', 'ano']


def test_listar_sem_catalogo_inicial_vem_vazio():
    app = create_app(dict(CONFIG_TESTE, CARREGAR_CATALOGO_INICIAL=False))
    corpo = app.test_client().get('/Eletronico').get_json()
    assert corpo == {'mensagem': 'Lista de eletronicos.', 'total': 0, 'dados': []}


def test_catalogo_inicial_nao_duplica(app):
    with app.app_context():
        assert carregar_catalogo_inicial() == 0
    assert app.test_client().get('/Eletronico').get_json()['total'] == len(CATALOGO_INICIAL)


def test_acentos_saem_legiveis(client):
    texto = client.get('/Eletronico').get_data(as_text=True)
    assert 'Periférico' in texto
    assert '\\u00e9' not in texto


# ---- GET /Eletronico/<id>

def test_buscar_por_id(client):
    resposta = client.get('/Eletronico/1')
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo['mensagem'] == 'Eletronico encontrado'
    assert corpo['eletronico']['id'] == 1
    assert corpo['eletronico']['nome'] == CATALOGO_INICIAL[0]['nome']


def test_buscar_id_inexistente_da_404_em_json(client):
    resposta = client.get('/Eletronico/999')
    assert resposta.status_code == 404
    assert resposta.get_json() == {'erro': 'Not Found', 'mensagem': 'Eletronico nao esta no catalogo.'}


def test_buscar_id_que_nao_e_numero_da_404_em_json(client):
    # <int:id> nao casa com 'abc', entao a rota nem existe
    resposta = client.get('/Eletronico/abc')
    assert resposta.status_code == 404
    assert resposta.get_json() == {'erro': 'Not Found', 'mensagem': 'Rota nao encontrada.'}


# ---- POST /Eletronico

def test_criar_eletronico(client):
    resposta = post(client, VALIDO)
    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo['mensagem'] == 'Eletronico cadastrado com sucesso'
    novo = corpo['eletronico']
    assert novo['id'] == len(CATALOGO_INICIAL) + 1
    assert resposta.headers['Location'].endswith('/Eletronico/%d' % novo['id'])
    assert {chave: novo[chave] for chave in VALIDO} == VALIDO

    assert client.get('/Eletronico/%d' % novo['id']).get_json()['eletronico'] == novo
    assert client.get('/Eletronico').get_json()['total'] == len(CATALOGO_INICIAL) + 1


def test_criar_apara_espacos_e_arredonda_preco(client):
    corpo = post(client, dict(VALIDO, nome='  Monitor  ', preco=899.999)).get_json()['eletronico']
    assert corpo['nome'] == 'Monitor'
    assert corpo['preco'] == 900.0


def test_criar_sem_campos_obrigatorios(client):
    resposta = post(client, {'nome': 'Monitor'})
    assert resposta.status_code == 400
    corpo = resposta.get_json()
    assert corpo['erro'] == 'Bad Request'
    assert corpo['mensagem'] == 'Dados invalidos.'
    assert corpo['detalhes'] == [
        'categoria e obrigatorio.',
        'modelo e obrigatorio.',
        'preco e obrigatorio.',
        'ano e obrigatorio.',
    ]
    assert client.get('/Eletronico').get_json()['total'] == len(CATALOGO_INICIAL)


@pytest.mark.parametrize('campo, valor, trecho', [
    ('nome', '', 'nome precisa ser um texto nao vazio.'),
    ('nome', '   ', 'nome precisa ser um texto nao vazio.'),
    ('nome', 123, 'nome precisa ser um texto nao vazio.'),
    ('nome', 'x' * 81, 'nome precisa ter no maximo 80 caracteres.'),
    ('categoria', None, 'categoria precisa ser um texto nao vazio.'),
    ('modelo', ['27'], 'modelo precisa ser um texto nao vazio.'),
    ('preco', 'caro', 'preco precisa ser um numero maior que zero.'),
    ('preco', 0, 'preco precisa ser um numero maior que zero.'),
    ('preco', -1, 'preco precisa ser um numero maior que zero.'),
    ('preco', True, 'preco precisa ser um numero maior que zero.'),
    ('ano', 'ontem', 'ano precisa ser um inteiro entre'),
    ('ano', 2024.0, 'ano precisa ser um inteiro entre'),
    ('ano', ANO_MINIMO - 1, 'ano precisa ser um inteiro entre'),
    ('ano', ano_maximo() + 1, 'ano precisa ser um inteiro entre'),
    ('ano', False, 'ano precisa ser um inteiro entre'),
])
def test_criar_com_campo_invalido(client, campo, valor, trecho):
    resposta = post(client, dict(VALIDO, **{campo: valor}))
    assert resposta.status_code == 400
    detalhes = resposta.get_json()['detalhes']
    assert len(detalhes) == 1
    assert trecho in detalhes[0]


def test_criar_aceita_limites_de_ano(client):
    assert post(client, dict(VALIDO, ano=ANO_MINIMO)).status_code == 201
    assert post(client, dict(VALIDO, ano=ano_maximo())).status_code == 201


def test_criar_com_campo_desconhecido(client):
    resposta = post(client, dict(VALIDO, cor='preto', voltagem=220))
    assert resposta.status_code == 400
    assert resposta.get_json()['detalhes'] == ['Campos desconhecidos: cor, voltagem.']


def test_criar_com_corpo_que_nao_e_objeto(client):
    for corpo in ([VALIDO], 'texto', 42, None):
        # json.dumps direto porque json=None no test_client significa "sem corpo"
        resposta = client.post('/Eletronico', data=json.dumps(corpo), content_type='application/json')
        assert resposta.status_code == 400
        assert resposta.get_json()['detalhes'] == ['O corpo precisa ser um objeto JSON com os campos do eletronico.']


def test_criar_com_json_mal_formado(client):
    resposta = client.post('/Eletronico', data='{"nome": ', content_type='application/json')
    assert resposta.status_code == 400
    assert resposta.get_json() == {
        'erro': 'Bad Request',
        'mensagem': 'Requisicao invalida. Confira se o JSON esta bem formado.',
    }


def test_criar_sem_content_type_json(client):
    resposta = client.post('/Eletronico', data='nome=Monitor')
    assert resposta.status_code == 415
    assert resposta.get_json() == {
        'erro': 'Unsupported Media Type',
        'mensagem': 'O corpo precisa ser JSON, enviado com Content-Type application/json.',
    }


# ---- PUT /Eletronico/<id>

def test_atualizar_parte_dos_campos(client):
    original = client.get('/Eletronico/1').get_json()['eletronico']
    resposta = client.put('/Eletronico/1', json={'preco': 1999.9, 'modelo': 'RTX 4060 Ti'})
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo['mensagem'] == 'Eletronico atualizado com sucesso'
    assert corpo['eletronico'] == dict(original, preco=1999.9, modelo='RTX 4060 Ti')
    assert client.get('/Eletronico/1').get_json()['eletronico'] == corpo['eletronico']


def test_atualizar_id_inexistente(client):
    resposta = client.put('/Eletronico/999', json={'preco': 10})
    assert resposta.status_code == 404
    assert resposta.get_json()['mensagem'] == 'Eletronico nao esta no catalogo.'


def test_atualizar_com_valor_invalido_nao_altera(client):
    original = client.get('/Eletronico/1').get_json()['eletronico']
    resposta = client.put('/Eletronico/1', json={'preco': -5, 'nome': ''})
    assert resposta.status_code == 400
    assert resposta.get_json()['detalhes'] == [
        'nome precisa ser um texto nao vazio.',
        'preco precisa ser um numero maior que zero.',
    ]
    assert client.get('/Eletronico/1').get_json()['eletronico'] == original


def test_atualizar_sem_nenhum_campo(client):
    resposta = client.put('/Eletronico/1', json={})
    assert resposta.status_code == 400
    assert resposta.get_json()['detalhes'] == ['Informe ao menos um campo para atualizar.']


def test_atualizar_sem_json(client):
    assert client.put('/Eletronico/1', data='x').status_code == 415


# ---- DELETE /Eletronico/<id>

def test_remover_eletronico(client):
    resposta = client.delete('/Eletronico/2')
    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert corpo['mensagem'] == 'Eletronico removido com sucesso'
    assert corpo['eletronico']['id'] == 2
    assert client.get('/Eletronico/2').status_code == 404
    assert client.get('/Eletronico').get_json()['total'] == len(CATALOGO_INICIAL) - 1


def test_remover_duas_vezes_da_404(client):
    assert client.delete('/Eletronico/2').status_code == 200
    resposta = client.delete('/Eletronico/2')
    assert resposta.status_code == 404
    assert resposta.get_json()['erro'] == 'Not Found'


# ---- erros gerais

def test_rota_inexistente_responde_json(client):
    resposta = client.get('/nada')
    assert resposta.status_code == 404
    assert resposta.mimetype == 'application/json'
    assert resposta.get_json() == {'erro': 'Not Found', 'mensagem': 'Rota nao encontrada.'}


def test_metodo_nao_permitido_responde_json(client):
    resposta = client.patch('/Eletronico')
    assert resposta.status_code == 405
    assert resposta.get_json() == {'erro': 'Method Not Allowed', 'mensagem': 'Metodo nao permitido para esta rota.'}
    assert 'GET' in resposta.headers['Allow'] and 'POST' in resposta.headers['Allow']


def test_erro_inesperado_vira_500_em_json(app):
    @app.route('/explode')
    def explode():
        raise RuntimeError('simulando um erro nao previsto')

    resposta = app.test_client().get('/explode')
    assert resposta.status_code == 500
    assert resposta.get_json() == {'erro': 'Internal Server Error', 'mensagem': 'Erro interno do servidor.'}
