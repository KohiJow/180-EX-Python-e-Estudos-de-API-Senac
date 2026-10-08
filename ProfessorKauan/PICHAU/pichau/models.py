from .db import db


class Eletronicos(db.Model):
    __tablename__ = 'eletronicos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'categoria': self.categoria,
            'preco': self.preco,
            'modelo': self.modelo,
            'ano': self.ano
        }
