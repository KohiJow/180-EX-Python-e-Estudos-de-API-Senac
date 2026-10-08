from db import db

class Carro(db.Model):  # Correção: "Model" com "M" maiúsculo
    __tablename__ = 'carros'  # Define o nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Correção: Define a chave primária corretamente
    modelo = db.Column(db.String(80), nullable=False)  # Correção: "Column" com "C" maiúsculo
    marca = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'marca': self.marca,
            'ano': self.ano
        }
