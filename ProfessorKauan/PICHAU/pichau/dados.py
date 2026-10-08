from .db import db
from .models import Eletronicos

# Catalogo de exemplo. Fica separado do codigo da API pra ser facil de trocar.
CATALOGO_INICIAL = [
    {'nome': 'Placa de video 8GB', 'categoria': 'Hardware', 'preco': 2299.90, 'modelo': 'RTX 4060', 'ano': 2023},
    {'nome': 'Processador 6 nucleos', 'categoria': 'Hardware', 'preco': 849.90, 'modelo': 'Ryzen 5 5600', 'ano': 2022},
    {'nome': 'Memoria RAM 16GB', 'categoria': 'Hardware', 'preco': 289.90, 'modelo': 'DDR4 3200MHz', 'ano': 2021},
    {'nome': 'SSD NVMe 1TB', 'categoria': 'Armazenamento', 'preco': 399.90, 'modelo': 'PCIe 4.0', 'ano': 2023},
    {'nome': 'Monitor 27 polegadas', 'categoria': 'Periférico', 'preco': 1199.00, 'modelo': 'IPS 165Hz', 'ano': 2024},
    {'nome': 'Teclado mecanico', 'categoria': 'Periférico', 'preco': 349.90, 'modelo': 'Switch red ABNT2', 'ano': 2023},
]


def carregar_catalogo_inicial():
    """Insere o catalogo so quando a tabela esta vazia. Devolve quantos itens entraram."""
    if db.session.execute(db.select(Eletronicos.id).limit(1)).first() is not None:
        return 0
    db.session.add_all(Eletronicos(**item) for item in CATALOGO_INICIAL)
    db.session.commit()
    return len(CATALOGO_INICIAL)
