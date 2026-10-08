from flask import Flask

from .db import db
from .routes import eletronicos_routes
from .erros import registrar_erros
from .dados import carregar_catalogo_inicial


def create_app(config=None):
    """Monta a aplicacao. `config` sobrescreve o padrao (os testes passam um banco em memoria)."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eletronicos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # catalogo de exemplo entra so na primeira execucao, quando a tabela esta vazia
    app.config['CARREGAR_CATALOGO_INICIAL'] = True
    if config:
        app.config.update(config)

    # acentos saem legiveis e os campos ficam na ordem em que foram montados
    app.json.ensure_ascii = False
    app.json.sort_keys = False

    db.init_app(app)
    app.register_blueprint(eletronicos_routes)
    registrar_erros(app)

    with app.app_context():
        db.create_all()
        if app.config['CARREGAR_CATALOGO_INICIAL']:
            carregar_catalogo_inicial()

    return app
