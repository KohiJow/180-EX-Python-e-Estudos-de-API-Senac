import os

from pichau import create_app

app = create_app()

if __name__ == '__main__':
    # PORT=8080 python app.py, quando a 5000 ja estiver ocupada
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
