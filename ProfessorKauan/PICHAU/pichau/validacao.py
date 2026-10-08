import math
from datetime import date

CAMPOS = ('nome', 'categoria', 'preco', 'modelo', 'ano')
CAMPOS_TEXTO = ('nome', 'categoria', 'modelo')
TAMANHO_MAXIMO = 80  # mesmo limite das colunas String(80)
ANO_MINIMO = 1950


def ano_maximo():
    # produto anunciado para o ano que vem ainda e valido
    return date.today().year + 1


def validar_eletronico(dados, parcial=False):
    """Confere o corpo de um POST (todos os campos) ou de um PUT (parcial=True, so os enviados).

    Devolve (limpo, erros): `limpo` tem apenas os campos aceitos, ja tratados;
    `erros` e uma lista de mensagens, vazia quando esta tudo certo.
    """
    if not isinstance(dados, dict):
        return {}, ['O corpo precisa ser um objeto JSON com os campos do eletronico.']

    erros = []
    limpo = {}

    desconhecidos = sorted(set(dados) - set(CAMPOS))
    if desconhecidos:
        erros.append('Campos desconhecidos: ' + ', '.join(desconhecidos) + '.')

    for campo in CAMPOS_TEXTO:
        if campo not in dados:
            if not parcial:
                erros.append(campo + ' e obrigatorio.')
            continue
        valor = dados[campo]
        if not isinstance(valor, str) or not valor.strip():
            erros.append(campo + ' precisa ser um texto nao vazio.')
        elif len(valor.strip()) > TAMANHO_MAXIMO:
            erros.append(campo + ' precisa ter no maximo %d caracteres.' % TAMANHO_MAXIMO)
        else:
            limpo[campo] = valor.strip()

    if 'preco' in dados:
        preco = dados['preco']
        # bool e subclasse de int, entao true passaria como 1 sem esse teste
        if isinstance(preco, bool) or not isinstance(preco, (int, float)) \
                or not math.isfinite(preco) or preco <= 0:
            erros.append('preco precisa ser um numero maior que zero.')
        else:
            limpo['preco'] = round(float(preco), 2)
    elif not parcial:
        erros.append('preco e obrigatorio.')

    if 'ano' in dados:
        ano = dados['ano']
        if isinstance(ano, bool) or not isinstance(ano, int) or not ANO_MINIMO <= ano <= ano_maximo():
            erros.append('ano precisa ser um inteiro entre %d e %d.' % (ANO_MINIMO, ano_maximo()))
        else:
            limpo['ano'] = ano
    elif not parcial:
        erros.append('ano e obrigatorio.')

    if parcial and not erros and not limpo:
        erros.append('Informe ao menos um campo para atualizar.')

    return limpo, erros
