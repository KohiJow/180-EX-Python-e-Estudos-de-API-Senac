# Python no Senac: exercícios, testes e APIs

Tudo que eu escrevi em Python durante o técnico no Senac, mais o que fiz por fora
estudando. São 217 arquivos `.py`, divididos por professor, porque foi assim que
as aulas aconteceram.

Não é um projeto único: é um caderno de código. Mantenho aqui porque mostra a
progressão, do `print('Hello, World!')` até API em Flask com teste automatizado.

Se você está avaliando o repositório pelo lado de QA, pule direto para
[Testes automatizados](#testes-automatizados) e [APIs em Flask](#apis-em-flask).
É a parte que tem a ver com o que eu faço hoje.

## Como rodar

Python 3.11 ou mais novo. A maior parte dos exercícios não tem dependência:

```bash
python3 "Professor Guanabara/ex045.py"
```

O que precisa de biblioteca está marcado em cada seção. Para instalar o que
aparece no repositório inteiro:

```bash
pip install requests pytest flask flask_sqlalchemy pygame PyQt5 selenium
```

## Testes automatizados

Pasta `Professor Gabriel`. Essa parte foi o primeiro contato com teste escrito em
código, e é a mais relevante do repositório.

| Arquivo | O que cobre |
| --- | --- |
| `app.py` | Classe `Calculator` com um método `evaluate_expression`, o alvo dos testes |
| `test_calculator_pytest.py` | Soma e subtração via pytest, com `@pytest.fixture` |
| `test_calculator_unitte_native.py` | Mesma lógica em `unittest`, incluindo divisão por zero e entrada inválida |
| `calculadoraFernando.py` | Calculadora em tkinter com a lógica isolada numa classe, justamente para poder testar sem abrir a janela |
| `test_calculadorainterfaceFernando.py` | Testa o fluxo de cliques (`1`, `+`, `2`, `=`) e o botão de limpar |
| `gerenciadordeanotacoesprf.py` | Gerenciador de notas em tkinter, com `add_note` e `delete_note` recebendo o listbox por parâmetro |
| `test_gerenciador_anotacoesprf.py` | pytest com `MagicMock` no listbox e `patch` nos diálogos do tkinter |
| `test_unittest` | A mesma suíte em `unittest`. Atenção: o arquivo não tem extensão `.py`, então o pytest não coleta ele |
| `gerenciadordeanotacoes_pyqt.py` | O mesmo gerenciador reescrito em PyQt5, como classe |

Os testes importam o módulo vizinho direto (`from app import Calculator`), então
rode de dentro da pasta:

```bash
cd "Professor Gabriel"
python -m pytest test_calculator_pytest.py test_calculadorainterfaceFernando.py
python -m unittest test_calculator_unitte_native.py
```

O que ficou de lição aqui: separar lógica de interface é o que torna o teste
possível. A `Calculator` do `calculadoraFernando.py` existe fora do tkinter de
propósito.

Também tem `selene.py`, um primeiro teste em Selenium que abre a tela de login do
Instagram no Edge e confere o `title`. Usa `time.sleep` e credencial de exemplo,
não é para rodar, é registro de como eu começei com browser.

## Consumo de API

`Professor Gabriel/request.py`: GET em `jsonplaceholder.typicode.com/users/10`
com `requests`, `raise_for_status()` e tratamento de `RequestException`.
Curto, mas é o esqueleto que eu uso até hoje em teste de API.

## APIs em Flask

Pasta `ProfessorKauan`. Duas APIs REST com SQLite, separadas em camadas
(`routes`, `controllers`, `models`, `db`).

### PICHAU: catálogo de eletrônicos

A mais completa das duas.

| Método | Rota | Comportamento |
| --- | --- | --- |
| GET | `/Eletronico` | Lista tudo |
| GET | `/Eletronico/<id>` | Retorna o item, ou 404 com mensagem se não existir |
| POST | `/Eletronico` | Exige `nome`, `categoria`, `preco`, `modelo`, `ano`. Falta um campo, responde 400 |

```bash
cd ProfessorKauan/PICHAU
python app.py
# em outro terminal
curl -s localhost:5000/Eletronico
curl -s -X POST localhost:5000/Eletronico \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Monitor","categoria":"Periferico","preco":899.9,"modelo":"27 polegadas","ano":2024}'
curl -s -i localhost:5000/Eletronico/999   # 404
```

### CARROS: cadastro de carros

Mais simples e inacabada. Só tem `POST /Carro`, que cadastra modelo, marca e ano.
Não existe GET, DELETE nem validação de campo obrigatório. Deixei como está por
ser o estado real em que a aula terminou.

```bash
cd ProfessorKauan/CARROS
python app.py
curl -s -X POST localhost:5000/Carro \
  -H 'Content-Type: application/json' \
  -d '{"modelo":"Gol","marca":"VW","ano":2015}'
```

O banco SQLite é criado na primeira execução, dentro de `instance/`. Não vai
versionado.

## Exercícios do curso do Guanabara

Pasta `Professor Guanabara`, 123 arquivos. Seguem a numeração do curso em vídeo.

| Faixa | Tema |
| --- | --- |
| `ex001` a `ex015` | Entrada e saída, operadores, conversão de tipo, contas (média, unidades, desconto, reajuste, Celsius para Fahrenheit) |
| `ex016` a `ex021` | Módulos `math`, `random` e `datetime`. O `ex021` toca um MP3 com `pygame` |
| `ex022` a `ex027` | Strings: `upper`, `lower`, `split`, `count`, `find`, fatiamento |
| `ex028` a `ex045` | Condições. `if` / `elif` / `else`, condições aninhadas, jogos com `random` (adivinhar número, jokenpô) |
| `ex046` a `ex071` | Repetição. `for`, `while`, acumulador, contador, menu, validação de entrada, caixa eletrônico |
| `ex072` a `ex077` | Tuplas |
| `ex078` a `ex088` | Listas, listas dentro de listas e matriz 3x3 |
| `ex089` a `ex095` | Listas e dicionários combinados: cadastro de aluno, de pessoa e aproveitamento de jogador |
| `ex096` a `ex113` | Funções: parâmetro opcional, `*args`, docstring, módulo próprio e pacote |

Arquivos de anotação soltos na mesma pasta: `Condicões.py`, `CondiçõesAninhadas.py`,
`Estrutura de Repetição.py`, `Manipulando Texto.py`, `a10.py` e `cor.py`
(tabela de cor ANSI para o terminal).

Honestidade sobre o que falta: `ex114` (testar se um site responde) e
`ex115a` / `ex115b` / `ex115c` (leitura e escrita de arquivo) têm só o enunciado,
sem solução. O `ex114` é o que mais me interessa hoje e é exatamente o que
acabei fazendo depois no `request.py`.

## Exercícios do professor Fernando

Pasta `Professor Fernando`, 70 arquivos. Numeração própria, foco em lista e laço
aplicados a situação de negócio (estoque, meta de venda, fatura, cadastro).

| Faixa | Tema |
| --- | --- |
| `ex001` a `ex005`, `DESAFIO01` a `DESAFIO03`, `TIPOSPRIMITIVOS.py` | Básico e tipos primitivos |
| `EX006` a `EX015` | Função com `def`, concatenação, f-string e formatação de alinhamento (`<`, `^`, `>`) |
| `EX016` a `EX033` | `for` e `while` sobre listas, `enumerate`, `break`, `continue`, `for` dentro de `for`. O `EX031` é uma calculadora com `try` / `except` |
| `EX034` a `EX053` | Listas: `append`, `pop`, índice negativo, `len`, `max`, `min`, `reduce` do `functools`. Termina em quatro exercícios maiores (estoque de papelaria, classificação de aluno, cadastro de evento, análise de fatura) |
| `EX054` a `EX059` | Dicionários |
| `EX060` a `EX065` | Tuplas |

Fora da faixa: `EX040` abre arquivo `.txt` com `with open` e trata
`FileNotFoundError`, e `EX041` é o exercício de `try` / `except` numa divisão.

`csv.py` é um rascunho abandonado de `pandas` com `matplotlib`. Não tem sintaxe
válida, nunca rodou. Deixei para não apagar histórico, mas não conte com ele.

## Contato

João Mateus Firmino Rodrigues, QA Engineer | contatojmfr@gmail.com
