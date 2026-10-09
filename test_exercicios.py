"""Garante que todo arquivo .py do repositorio continua compilando.

Nao roda os exercicios (quase todos pedem input), mas pega erro de sintaxe
e caminho com escape invalido, que foram os problemas que apareceram.
"""
import pathlib

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent
PASTAS = ['Professor Guanabara', 'Professor Fernando', 'Professor Gabriel', 'ProfessorKauan']

# rascunho de pandas que nunca teve sintaxe valida; o README explica
IGNORAR = {RAIZ / 'Professor Fernando' / 'csv.py'}

ARQUIVOS = sorted(
    arquivo
    for pasta in PASTAS
    for arquivo in (RAIZ / pasta).rglob('*.py')
    if arquivo not in IGNORAR
)


def test_encontrou_os_exercicios():
    assert len(ARQUIVOS) > 200


@pytest.mark.parametrize('arquivo', ARQUIVOS, ids=lambda caminho: str(caminho.relative_to(RAIZ)))
def test_compila(arquivo):
    compile(arquivo.read_bytes(), str(arquivo), 'exec')
