from flask import jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES


def resposta_erro(status, mensagem, detalhes=None):
    """Formato unico de erro: {"erro": nome HTTP, "mensagem": texto, "detalhes": [...] (opcional)}."""
    corpo = {'erro': HTTP_STATUS_CODES.get(status, 'Error'), 'mensagem': mensagem}
    if detalhes:
        corpo['detalhes'] = detalhes
    return jsonify(corpo), status


# Os textos padrao do Flask para esses casos vem em ingles e em HTML; aqui eles viram
# a mesma resposta JSON das outras rotas, em portugues.
MENSAGENS = {
    400: 'Requisicao invalida. Confira se o JSON esta bem formado.',
    404: 'Rota nao encontrada.',
    405: 'Metodo nao permitido para esta rota.',
    415: 'O corpo precisa ser JSON, enviado com Content-Type application/json.',
}


def registrar_erros(app):
    @app.errorhandler(HTTPException)
    def erro_http(e):
        # rota inexistente (404), metodo errado (405), corpo sem JSON (415), JSON mal formado (400)...
        # Os cabecalhos que o Flask poe (ex.: Allow do 405) sao mantidos.
        resposta, status = resposta_erro(e.code, MENSAGENS.get(e.code, e.description))
        resposta.status_code = status
        resposta.headers.extend(cabecalho for cabecalho in e.get_headers() if cabecalho[0] != 'Content-Type')
        return resposta

    @app.errorhandler(Exception)
    def erro_interno(e):
        app.logger.exception('erro nao tratado na requisicao')
        return resposta_erro(500, 'Erro interno do servidor.')
