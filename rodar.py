"""Roda um exercicio pelo numero, sem precisar digitar o caminho com espaco.

    python rodar.py guanabara 45          roda "Professor Guanabara/ex045.py"
    python rodar.py fernando 31           roda "Professor Fernando/EX031.py"
    python rodar.py fernando desafio02    roda "Professor Fernando/DESAFIO02.py"
    python rodar.py guanabara 115a        roda "Professor Guanabara/ex115a.py"
    python rodar.py gabriel --lista       mostra os arquivos da pasta

O exercicio roda com a pasta dele como diretorio atual, entao arquivos
que ele abre pelo nome (ex021.mp3, arquivo.txt) sao encontrados.
"""
import argparse
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

PASTAS = {
    'guanabara': 'Professor Guanabara',
    'fernando': 'Professor Fernando',
    'gabriel': 'Professor Gabriel',
}

# ex045, EX006, ex115a: prefixo "ex", numero e um sufixo opcional de letras
PADRAO_NUMERADO = re.compile(r'^(?:ex)?(\d+)([a-z]*)$')


def chave(nome):
    """Forma comparavel de um nome de exercicio: ('ex', 45, '') para ex045.py,
    ('nome', 'desafio01') para DESAFIO01.py. Ignora extensao e maiusculas."""
    nome = nome.lower()
    if nome.endswith('.py'):
        nome = nome[:-3]
    casou = PADRAO_NUMERADO.match(nome)
    if casou:
        return ('ex', int(casou.group(1)), casou.group(2))
    return ('nome', nome)


def listar_exercicios(pasta):
    # sem distinguir maiusculas: ex001..ex005 e EX006..EX065 ficam juntos na listagem
    return sorted((arquivo for arquivo in os.listdir(pasta) if arquivo.endswith('.py')), key=str.lower)


def encontrar_exercicio(pedido, arquivos):
    """Devolve o arquivo que corresponde ao pedido ('45', '045', 'EX45', 'ex045.py',
    'desafio01'...) ou None quando nenhum casa."""
    alvo = chave(pedido)
    for arquivo in arquivos:
        if chave(arquivo) == alvo:
            return arquivo
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description='Roda um exercicio do repositorio pelo numero.')
    parser.add_argument('professor', choices=sorted(PASTAS), help='pasta do professor')
    parser.add_argument('exercicio', nargs='?', help='numero (45, 045, ex045) ou nome (desafio01, cor)')
    parser.add_argument('--lista', action='store_true', help='so lista os arquivos da pasta')
    args = parser.parse_args(argv)

    pasta = os.path.join(RAIZ, PASTAS[args.professor])
    arquivos = listar_exercicios(pasta)

    if args.lista or not args.exercicio:
        print('\n'.join(arquivos))
        return 0

    arquivo = encontrar_exercicio(args.exercicio, arquivos)
    if arquivo is None:
        print('Nao achei "%s" em "%s". Use --lista para ver o que existe.'
              % (args.exercicio, PASTAS[args.professor]), file=sys.stderr)
        return 2

    print('>>> %s/%s' % (PASTAS[args.professor], arquivo), file=sys.stderr)
    return subprocess.call([sys.executable, arquivo], cwd=pasta)


if __name__ == '__main__':
    sys.exit(main())
