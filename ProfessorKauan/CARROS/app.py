# Importa a classe Flask, que é a principal classe para criar o aplicativo web.
from flask import Flask 

# Importa a instância do banco de dados (db), que será usada para interagir com o banco de dados.
from db import db

# Importa o Blueprint de rotas relacionadas aos carros, que definimos anteriormente.
from routes.carro_routes import carro_routes

# Cria uma instância do aplicativo Flask, que é a base para a aplicação web.
app = Flask(__name__)

# Configura a URI de conexão com o banco de dados, neste caso, um banco de dados SQLite.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carros.db"

# Desativa o rastreamento de modificações no banco de dados para evitar um overhead desnecessário.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Correção

# Inicializa o banco de dados com a aplicação Flask, permitindo que o Flask interaja com o banco.
db.init_app(app)

# Registra o Blueprint de rotas de carros no aplicativo Flask.
app.register_blueprint(carro_routes)  # Correção

# Bloco principal do aplicativo Flask.
if __name__ == "__main__":
    
    # O Bloco 'with app.app_context()' é usado para criar o banco de dados antes de rodar a aplicação.
    # Ele garante que a criação das tabelas do banco de dados ocorra dentro do contexto da aplicação Flask.
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados com base nos modelos definidos.

    # Inicia o servidor web do Flask em modo de desenvolvimento, permitindo a depuração.
    # O servidor rodará em http://127.0.0.1:5000 por padrão, e o 'debug=True' permite ver logs de erros e atualizações automáticas.    
    app.run(debug=True)
