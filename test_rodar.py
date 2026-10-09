import os
import subprocess
import sys

import pytest

import rodar

ARQUIVOS = ['ex001.py', 'ex044.py', 'ex045.py', 'ex115a.py', 'ex115b.py', 'EX007.py', 'DESAFIO01.py', 'cor.py']


@pytest.mark.parametrize('nome, esperado', [
    ('ex045.py', ('ex', 45, '')),
    ('EX006.py', ('ex', 6, '')),
    ('ex115a.py', ('ex', 115, 'a')),
    ('45', ('ex', 45, '')),
    ('045', ('ex', 45, '')),
    ('EX45', ('ex', 45, '')),
    ('DESAFIO01.py', ('nome', 'desafio01')),
    ('cor', ('nome', 'cor')),
])
def test_chave(nome, esperado):
    assert rodar.chave(nome) == esperado


@pytest.mark.parametrize('pedido, esperado', [
    ('45', 'ex045.py'),
    ('045', 'ex045.py'),
    ('EX45', 'ex045.py'),
    ('ex045.py', 'ex045.py'),
    ('7', 'EX007.py'),
    ('115a', 'ex115a.py'),
    ('115B', 'ex115b.py'),
    ('desafio01', 'DESAFIO01.py'),
    ('Cor', 'cor.py'),
    ('115', None),
    ('999', None),
    ('nada', None),
])
def test_encontrar_exercicio(pedido, esperado):
    assert rodar.encontrar_exercicio(pedido, ARQUIVOS) == esperado


def test_pastas_existem():
    for pasta in rodar.PASTAS.values():
        assert os.path.isdir(os.path.join(rodar.RAIZ, pasta))


def test_lista_le_a_pasta_real():
    arquivos = rodar.listar_exercicios(os.path.join(rodar.RAIZ, rodar.PASTAS['guanabara']))
    assert 'ex001.py' in arquivos and 'ex115c.py' in arquivos
    assert all(arquivo.endswith('.py') for arquivo in arquivos)
    assert rodar.encontrar_exercicio('45', arquivos) == 'ex045.py'


def rodar_cli(*argumentos, entrada=None):
    # sem `entrada` o stdin vai fechado: um exercicio que pede input() termina
    # com EOFError em vez de ficar esperando o terminal
    return subprocess.run(
        [sys.executable, os.path.join(rodar.RAIZ, 'rodar.py')] + list(argumentos),
        input=entrada, stdin=None if entrada is not None else subprocess.DEVNULL,
        capture_output=True, text=True, timeout=30,
    )


def test_cli_roda_exercicio_sem_entrada():
    resultado = rodar_cli('guanabara', '1')
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == 'Hello, World!'
    assert 'Professor Guanabara/ex001.py' in resultado.stderr

    resultado = rodar_cli('fernando', '001')
    assert resultado.returncode == 0
    assert resultado.stdout.strip() == 'Olá, mundo!'


def test_cli_repassa_a_entrada_para_o_exercicio():
    resultado = rodar_cli('guanabara', '2', entrada='Maria\n')
    assert resultado.returncode == 0
    assert resultado.stdout.strip().endswith('Olá Maria!')


def test_cli_repassa_o_codigo_de_saida():
    # ex002 pede input(); com o stdin fechado ele morre com EOFError e o rodar
    # tem que devolver o mesmo codigo de saida do exercicio
    resultado = rodar_cli('guanabara', '2')
    assert resultado.returncode == 1
    assert 'EOFError' in resultado.stderr


def test_cli_exercicio_inexistente():
    resultado = rodar_cli('guanabara', '999')
    assert resultado.returncode == 2
    assert 'Nao achei "999"' in resultado.stderr


def test_cli_lista():
    resultado = rodar_cli('fernando', '--lista')
    assert resultado.returncode == 0
    linhas = resultado.stdout.split()
    assert 'EX031.py' in linhas and 'DESAFIO01.py' in linhas
    assert rodar_cli('fernando').stdout == resultado.stdout
